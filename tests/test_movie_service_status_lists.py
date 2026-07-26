import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.movie_metadata_repository import MovieMetadataRepository
from app.movie_repository import MovieRepository
from app.movie_service import MovieService
from app.movie_status import MovieStatus
from app.user_movie_repository import UserMovieRepository


class FakeTMDBClient:
    pass


class MovieServiceStatusListTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        database_path = (
            Path(self.temporary_directory.name)
            / "movie_status_lists_test.db"
        )
        database_path_patch = patch.object(
            database,
            "DATABASE_PATH",
            database_path,
        )
        database_path_patch.start()
        self.addCleanup(database_path_patch.stop)

        initialize_database()

        self.movie_repository = MovieRepository()
        self.metadata_repository = MovieMetadataRepository()
        self.user_repository = UserMovieRepository()
        self.service = MovieService(
            movie_repository=self.movie_repository,
            user_repository=self.user_repository,
            metadata_repository=self.metadata_repository,
            tmdb_client=FakeTMDBClient(),
        )

        statuses = [
            MovieStatus.WATCHED,
            MovieStatus.REWATCH,
            MovieStatus.WATCH_LATER,
            MovieStatus.EXCLUDED,
            MovieStatus.NEW_DISCOVERY,
        ]

        for tmdb_id, status in enumerate(statuses, start=101):
            self.movie_repository.save_movie(
                {
                    "id": tmdb_id,
                    "title": f"Movie {tmdb_id}",
                    "original_title": f"Movie {tmdb_id}",
                    "release_date": "2020-01-01",
                    "overview": "Test movie.",
                    "poster_path": None,
                    "backdrop_path": None,
                    "vote_average": 7.0,
                }
            )
            self.user_repository.set_status(tmdb_id, status)

        self.metadata_repository.replace_movie_genres(
            101,
            [{"id": 878, "name": "Science Fiction"}],
        )
        self.metadata_repository.replace_movie_genres(
            102,
            [{"id": 18, "name": "Drama"}],
        )
        self.metadata_repository.replace_movie_genres(
            103,
            [{"id": 53, "name": "Thriller"}],
        )
        self.metadata_repository.replace_movie_genres(
            104,
            [{"id": 27, "name": "Horror"}],
        )

    def _assert_enriched(
        self,
        movie: dict,
        expected_status: MovieStatus,
    ) -> None:
        self.assertIn("genres", movie)
        self.assertEqual(
            movie["user_data"]["status"],
            expected_status.value,
        )

    def test_watched_list_includes_genres_and_user_data(self) -> None:
        movies = self.service.get_watched_movies()
        movies_by_id = {
            movie["tmdb_id"]: movie
            for movie in movies
        }

        self.assertEqual(set(movies_by_id), {101, 102})
        self._assert_enriched(
            movies_by_id[101],
            MovieStatus.WATCHED,
        )
        self._assert_enriched(
            movies_by_id[102],
            MovieStatus.REWATCH,
        )
        self.assertEqual(
            movies_by_id[101]["genres"][0]["name"],
            "Science Fiction",
        )

    def test_other_status_lists_are_enriched(self) -> None:
        watch_later = self.service.get_watchlist_movies()[0]
        rewatch = self.service.get_rewatch_movies()[0]
        excluded = self.service.get_excluded_movies()[0]
        new_discovery = self.service.get_new_discovery_movies()[0]

        self._assert_enriched(
            watch_later,
            MovieStatus.WATCH_LATER,
        )
        self._assert_enriched(
            rewatch,
            MovieStatus.REWATCH,
        )
        self._assert_enriched(
            excluded,
            MovieStatus.EXCLUDED,
        )
        self._assert_enriched(
            new_discovery,
            MovieStatus.NEW_DISCOVERY,
        )
        self.assertEqual(new_discovery["genres"], [])

    def test_generic_status_list_is_an_exact_match(self) -> None:
        watched = self.service.get_movies_by_status("watched")
        rewatch = self.service.get_movies_by_status("rewatch")

        self.assertEqual(
            [movie["tmdb_id"] for movie in watched],
            [101],
        )
        self.assertEqual(
            [movie["tmdb_id"] for movie in rewatch],
            [102],
        )
        self._assert_enriched(watched[0], MovieStatus.WATCHED)
        self._assert_enriched(rewatch[0], MovieStatus.REWATCH)

    def test_generic_status_list_rejects_invalid_status(self) -> None:
        with self.assertRaises(ValueError):
            self.service.get_movies_by_status("maybe")


if __name__ == "__main__":
    unittest.main()
