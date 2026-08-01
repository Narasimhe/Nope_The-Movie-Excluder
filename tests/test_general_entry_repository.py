import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.general_entry_repository import GeneralEntryRepository


class GeneralEntryRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        path = Path(self.temporary_directory.name) / "entries.db"
        database_patch = patch.object(database, "DATABASE_PATH", path)
        database_patch.start()
        self.addCleanup(database_patch.stop)
        initialize_database()
        self.repository = GeneralEntryRepository()

    def test_entries_are_created_updated_filtered_and_soft_deleted(self) -> None:
        note = self.repository.create_entry(
            "note", "Space terms", "- deep-space\n- starship"
        )
        link = self.repository.create_entry(
            "link", "Slow-burn site", "Useful source", "example.com"
        )

        results = self.repository.list_entries()
        self.assertEqual(results["total_results"], 2)
        self.assertEqual(results["results"][0]["entry_id"], link["entry_id"])
        self.assertEqual(
            self.repository.list_entries(entry_type="note")["results"][0]["title"],
            "Space terms",
        )
        updated = self.repository.update_entry(
            note["entry_id"], "note", "Space travel terms", "cryogenic-sleep"
        )
        self.assertEqual(updated["title"], "Space travel terms")
        self.assertEqual(
            self.repository.list_entries(query="cryogenic")["total_results"],
            1,
        )
        self.assertTrue(self.repository.delete_entry(link["entry_id"]))
        self.assertIsNone(self.repository.get_entry(link["entry_id"]))

    def test_entries_are_paginated_twenty_at_a_time(self) -> None:
        for number in range(21):
            self.repository.create_entry("note", f"Note {number}")
        first = self.repository.list_entries(page=1)
        second = self.repository.list_entries(page=2)
        self.assertEqual(len(first["results"]), 20)
        self.assertEqual(len(second["results"]), 1)
        self.assertEqual(first["total_pages"], 2)

    def test_link_requires_a_url(self) -> None:
        with self.assertRaisesRegex(ValueError, "needs a URL"):
            self.repository.create_entry("link", "Missing")


if __name__ == "__main__":
    unittest.main()
