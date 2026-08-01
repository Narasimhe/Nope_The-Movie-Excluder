import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.search_state_repository import SearchStateRepository


class SearchStateRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        path = Path(self.temporary_directory.name) / "search_state.db"
        database_patch = patch.object(database, "DATABASE_PATH", path)
        database_patch.start()
        self.addCleanup(database_patch.stop)
        initialize_database()
        self.repository = SearchStateRepository()

    def test_unsaved_search_state_is_remembered(self) -> None:
        saved = self.repository.save_state(
            mode="super",
            filters={"include_genre_ids": [878]},
            personal_filters={
                "included_statuses": ["watch_later"],
                "include_untracked": False,
                "favorite_only": False,
                "notes_query": None,
            },
            selected_preference_id=None,
            filters_collapsed=True,
        )
        self.assertEqual(saved["mode"], "super")
        self.assertEqual(saved["filters"]["include_genre_ids"], [878])
        self.assertTrue(saved["filters_collapsed"])
        self.assertEqual(self.repository.get_state(), saved)

    def test_invalid_mode_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Search mode"):
            self.repository.save_state(
                mode="mystery",
                filters={},
                personal_filters=None,
                selected_preference_id=None,
                filters_collapsed=False,
            )


if __name__ == "__main__":
    unittest.main()
