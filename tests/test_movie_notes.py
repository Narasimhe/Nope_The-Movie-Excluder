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
        raise AssertionError("The notes tests must remain local.")


class MovieNotesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        database_path = (
            Path(self.temporary_directory.name)
            / "movie_notes_test.db"
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

        for movie_id, title in (
            (101, "Cold Film"),
            (202, "Warm Film"),
            (303, "Percentage Film"),
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

        self.user_repository.set_status(
            101,
            MovieStatus.NEW_DISCOVERY,
        )
        self.user_repository.set_status(
            202,
            MovieStatus.WATCHED,
        )
        self.user_repository.set_status(
            303,
            MovieStatus.EXCLUDED,
        )
        self.user_repository.set_notes(
            101,
            "Beautiful cold ambience and quiet streets.",
        )
        self.user_repository.set_notes(
            202,
            "Warm daylight and quick pacing.",
        )
        self.user_repository.set_notes(
            303,
            "A 100% literal observation.",
        )

        self.service = MovieService(
            movie_repository=self.movie_repository,
            user_repository=self.user_repository,
            metadata_repository=self.metadata_repository,
            tmdb_client=NoTMDBClient(),
        )

    def test_notes_search_is_case_insensitive_and_partial(self) -> None:
        matches = self.user_repository.search_notes("COLD ambience")

        self.assertEqual(
            [match["tmdb_id"] for match in matches],
            [101],
        )

    def test_notes_search_treats_wildcards_as_text(self) -> None:
        matches = self.user_repository.search_notes("%")

        self.assertEqual(
            [match["tmdb_id"] for match in matches],
            [303],
        )

    def test_empty_notes_search_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.user_repository.search_notes("   ")

    def test_service_returns_movies_with_personal_data(self) -> None:
        results = self.service.search_movie_notes("quiet streets")

        self.assertEqual(
            [movie["tmdb_id"] for movie in results],
            [101],
        )
        self.assertEqual(
            results[0]["user_data"]["status"],
            MovieStatus.NEW_DISCOVERY.value,
        )
        self.assertIn(
            "cold ambience",
            results[0]["user_data"]["notes"],
        )

    def test_notes_can_be_updated_and_cleared(self) -> None:
        updated = self.service.set_movie_notes(
            101,
            "  Keep this one.  ",
        )
        cleared = self.service.set_movie_notes(101, "   ")

        self.assertEqual(updated["notes"], "Keep this one.")
        self.assertIsNone(cleared["notes"])


if __name__ == "__main__":
    unittest.main()
