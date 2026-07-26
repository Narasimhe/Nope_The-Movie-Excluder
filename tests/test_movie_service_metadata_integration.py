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
    def __init__(self) -> None:
        self.movie_detail_calls = 0

    def get_movie(self, movie_id: int) -> dict:
        self.movie_detail_calls += 1

        return {
            "id": movie_id,
            "title": "Arrival",
            "original_title": "Arrival",
            "release_date": "2016-11-11",
            "overview": "A linguist communicates with visitors.",
            "poster_path": "/arrival.jpg",
            "backdrop_path": "/arrival-backdrop.jpg",
            "vote_average": 7.6,
            "genres": [
                {"id": 18, "name": "Drama"},
                {"id": 878, "name": "Science Fiction"},
            ],
            "keywords": {
                "keywords": [
                    {"id": number, "name": f"Keyword {number}"}
                    for number in range(1, 8)
                ]
            },
        }


class MovieServiceMetadataIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        database_path = (
            Path(self.temporary_directory.name)
            / "movie_service_metadata_test.db"
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
        self.tmdb_client = FakeTMDBClient()
        self.service = MovieService(
            movie_repository=self.movie_repository,
            user_repository=UserMovieRepository(),
            metadata_repository=self.metadata_repository,
            tmdb_client=self.tmdb_client,
        )

    def test_opening_details_saves_genres_and_top_five_keywords(
        self,
    ) -> None:
        movie = self.service.get_movie(329865)

        self.assertEqual(self.tmdb_client.movie_detail_calls, 1)
        self.assertEqual(
            {
                genre["tmdb_genre_id"]
                for genre in movie["genres"]
            },
            {18, 878},
        )
        self.assertEqual(len(movie["keywords"]), 5)
        self.assertEqual(
            [
                keyword["tmdb_keyword_id"]
                for keyword in movie["keywords"]
            ],
            [1, 2, 3, 4, 5],
        )
        self.assertIsNotNone(movie["metadata_fetched_at"])

    def test_second_open_uses_saved_metadata(self) -> None:
        self.service.get_movie(329865)
        second_result = self.service.get_movie(329865)

        self.assertEqual(self.tmdb_client.movie_detail_calls, 1)
        self.assertEqual(len(second_result["genres"]), 2)
        self.assertEqual(len(second_result["keywords"]), 5)

    def test_old_saved_movie_is_enriched_when_opened(self) -> None:
        self.movie_repository.save_movie(
            {
                "id": 329865,
                "title": "Arrival",
                "original_title": "Arrival",
                "release_date": "2016-11-11",
                "overview": "Previously saved movie.",
                "poster_path": None,
                "backdrop_path": None,
                "vote_average": 7.6,
            }
        )
        custom = self.metadata_repository.add_custom_keyword(
            329865,
            "cold ambience",
        )

        movie = self.service.get_movie(329865)

        self.assertEqual(self.tmdb_client.movie_detail_calls, 1)
        self.assertIn(custom, movie["keywords"])
        self.assertEqual(
            len(
                [
                    keyword
                    for keyword in movie["keywords"]
                    if not keyword["is_custom"]
                ]
            ),
            5,
        )

    def test_service_adds_and_removes_a_custom_keyword(self) -> None:
        added = self.service.add_custom_keyword(
            329865,
            "cold ambience",
        )

        self.assertTrue(added["is_custom"])
        self.assertEqual(added["name"], "cold ambience")
        self.assertEqual(self.tmdb_client.movie_detail_calls, 1)

        removed = self.service.remove_custom_keyword(
            329865,
            added["keyword_id"],
        )

        self.assertTrue(removed)
        self.assertEqual(
            self.metadata_repository.get_custom_keywords(329865),
            [],
        )

    def test_status_selection_caches_an_uncached_movie(self) -> None:
        result = self.service.set_movie_status(
            329865,
            MovieStatus.WATCH_LATER,
        )

        self.assertEqual(
            result["status"],
            MovieStatus.WATCH_LATER.value,
        )
        self.assertEqual(self.tmdb_client.movie_detail_calls, 1)
        self.assertIsNotNone(
            self.movie_repository.get_movie(329865)
        )

        changed = self.service.set_movie_status(
            329865,
            MovieStatus.EXCLUDED,
        )

        self.assertEqual(
            changed["status"],
            MovieStatus.EXCLUDED.value,
        )
        self.assertEqual(self.tmdb_client.movie_detail_calls, 1)

        movie_details = self.service.get_movie(329865)

        self.assertEqual(
            movie_details["user_data"]["status"],
            MovieStatus.EXCLUDED.value,
        )
        self.assertEqual(self.tmdb_client.movie_detail_calls, 1)

    def test_invalid_status_does_not_fetch_the_movie(self) -> None:
        with self.assertRaisesRegex(ValueError, "Invalid movie status"):
            self.service.set_movie_status(329865, "maybe")

        self.assertEqual(self.tmdb_client.movie_detail_calls, 0)
        self.assertIsNone(
            self.movie_repository.get_movie(329865)
        )


if __name__ == "__main__":
    unittest.main()
