import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.general_entry_repository import GeneralEntryRepository
from app.movie_metadata_repository import MovieMetadataRepository
from app.movie_repository import MovieRepository
from app.movie_status import MovieStatus
from app.storage_repository import StorageRepository
from app.user_movie_repository import UserMovieRepository


class StorageRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        path = Path(self.temporary_directory.name) / "storage.db"
        database_patch = patch.object(database, "DATABASE_PATH", path)
        database_patch.start()
        self.addCleanup(database_patch.stop)
        initialize_database()
        self.movies = MovieRepository()
        self.storage = StorageRepository()

    def _save_movie(self, movie_id: int) -> None:
        self.movies.save_movie({
            "id": movie_id,
            "title": f"Movie {movie_id}",
            "release_date": "2020-01-01",
        })

    def test_cleanup_removes_only_old_tmdb_only_cache(self) -> None:
        for movie_id in range(1, 5):
            self._save_movie(movie_id)
        UserMovieRepository().set_status(2, MovieStatus.WATCHED)
        MovieMetadataRepository().add_custom_keyword(3, "personal")
        with database.get_connection() as connection:
            connection.execute(
                "UPDATE movies SET last_accessed_at = '2020-01-01 00:00:00' WHERE tmdb_id < 4"
            )

        result = self.storage.cleanup_old_cache(90)

        self.assertEqual(result["removed_movies"], 1)
        self.assertIsNone(self.movies.get_movie(1))
        for movie_id in (2, 3, 4):
            self.assertIsNotNone(self.movies.get_movie(movie_id))

    def test_deleted_general_entries_can_be_purged(self) -> None:
        entries = GeneralEntryRepository()
        entry = entries.create_entry("note", "Disposable", tags=["cleanup"])
        entries.delete_entry(entry["entry_id"])

        result = self.storage.purge_deleted_entries()
        summary = self.storage.get_summary()

        self.assertEqual(result["removed_entries"], 1)
        self.assertEqual(summary["soft_deleted_entries"], 0)


if __name__ == "__main__":
    unittest.main()
