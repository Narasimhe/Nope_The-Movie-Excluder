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


class NoTMDBClient:
    def get_movie(self, movie_id: int) -> dict:
        raise AssertionError("Favorite tests must remain local.")


class FavoriteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        database_path = (
            Path(self.temporary_directory.name)
            / "favorites_test.db"
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
        self.user_repository = UserMovieRepository()
        self.metadata_repository = MovieMetadataRepository()
        self.service = MovieService(
            movie_repository=self.movie_repository,
            user_repository=self.user_repository,
            metadata_repository=self.metadata_repository,
            tmdb_client=NoTMDBClient(),
        )

        for movie_id, title in (
            (101, "Favorite Watched Movie"),
            (202, "Favorite Watch-Later Movie"),
            (303, "Ordinary Movie"),
        ):
            self.movie_repository.save_movie(
                {
                    "id": movie_id,
                    "title": title,
                    "original_title": title,
                    "release_date": "2020-01-01",
                    "overview": None,
                    "poster_path": None,
                    "backdrop_path": None,
                    "vote_average": 7.0,
                }
            )

        self.user_repository.set_status(101, MovieStatus.WATCHED)
        self.user_repository.set_status(
            202,
            MovieStatus.WATCH_LATER,
        )
        self.user_repository.set_status(
            303,
            MovieStatus.NEW_DISCOVERY,
        )

    def test_favorite_is_independent_from_status(self) -> None:
        favorited = self.service.set_movie_favorite(101, True)
        changed = self.user_repository.set_status(
            101,
            MovieStatus.REWATCH,
        )

        self.assertTrue(favorited["is_favorite"])
        self.assertTrue(changed["is_favorite"])
        self.assertEqual(changed["status"], "rewatch")

    def test_favorites_list_includes_different_statuses(self) -> None:
        self.service.set_movie_favorite(101, True)
        self.user_repository.set_status(101, MovieStatus.REWATCH)
        self.user_repository.set_status(202, MovieStatus.WATCHED)
        watched_favorite = self.service.set_movie_favorite(
            202,
            True,
        )

        favorites = self.service.get_favorite_movies()

        self.assertEqual(
            {movie["tmdb_id"] for movie in favorites},
            {101, 202},
        )
        self.assertTrue(
            all(
                movie["user_data"]["is_favorite"]
                for movie in favorites
            )
        )
        self.assertEqual(
            watched_favorite["status"],
            MovieStatus.WATCHED.value,
        )

    def test_unwatched_movie_cannot_be_favorited(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "Only watched",
        ):
            self.service.set_movie_favorite(303, True)

        result = self.user_repository.get_user_movie_data(303)
        watched_ids = {
            movie["tmdb_id"]
            for movie in self.service.get_watched_movies()
        }

        self.assertEqual(
            result["status"],
            MovieStatus.NEW_DISCOVERY.value,
        )
        self.assertFalse(result["is_favorite"])
        self.assertNotIn(303, watched_ids)

    def test_untracked_movie_cannot_be_favorited(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "Only watched",
        ):
            self.service.set_movie_favorite(999, True)

        self.assertIsNone(
            self.user_repository.get_user_movie_data(999)
        )

    def test_unwatched_status_removes_favorite(self) -> None:
        self.service.set_movie_favorite(101, True)
        changed = self.user_repository.set_status(
            101,
            MovieStatus.WATCH_LATER,
        )

        self.assertEqual(changed["status"], "watch_later")
        self.assertFalse(changed["is_favorite"])
        self.assertEqual(self.service.get_favorite_movies(), [])

    def test_movie_can_be_removed_from_favorites(self) -> None:
        self.service.set_movie_favorite(101, True)
        result = self.service.set_movie_favorite(101, False)

        self.assertFalse(result["is_favorite"])
        self.assertEqual(self.service.get_favorite_movies(), [])

    def test_favorite_requires_a_boolean(self) -> None:
        with self.assertRaises(ValueError):
            self.service.set_movie_favorite(101, 1)


if __name__ == "__main__":
    unittest.main()
