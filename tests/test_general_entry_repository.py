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

    def test_link_entry_accepts_multiple_urls(self) -> None:
        entry = self.repository.create_entry(
            "link",
            "Reference sites",
            "Two useful sources",
            " example.com/one \n\n https://example.org/two ",
        )

        self.assertEqual(
            entry["url"],
            "example.com/one\nhttps://example.org/two",
        )

    def test_entry_tags_are_reusable_searchable_and_replaceable(self) -> None:
        first = self.repository.create_entry(
            "note",
            "AI coding",
            "Private thoughts",
            tags=["AI", "Coding", "ai"],
        )
        second = self.repository.create_entry(
            "link",
            "Python reference",
            "Useful source",
            "example.com",
            tags=["Coding", "Python"],
        )

        self.assertEqual(
            [tag["name"] for tag in first["tags"]],
            ["AI", "Coding"],
        )
        coding = self.repository.list_entries(tag="coding")
        self.assertEqual(coding["total_results"], 2)
        self.assertEqual(
            self.repository.list_entries(query="Python")["results"][0]["entry_id"],
            second["entry_id"],
        )

        updated = self.repository.update_entry(
            first["entry_id"],
            "note",
            "AI coding",
            "Private thoughts",
            tags=["Machine Learning"],
        )
        self.assertEqual(
            [tag["name"] for tag in updated["tags"]],
            ["Machine Learning"],
        )
        self.assertEqual(
            self.repository.list_entries(tag="AI")["total_results"],
            0,
        )

    def test_recently_updated_entries_sort_first(self) -> None:
        older = self.repository.create_entry("note", "Older")
        newer = self.repository.create_entry("note", "Newer")
        with database.get_connection() as connection:
            connection.execute(
                "UPDATE general_entries SET updated_at = ? WHERE entry_id = ?",
                ("2030-01-01 00:00:00", older["entry_id"]),
            )
        results = self.repository.list_entries()["results"]
        self.assertEqual(results[0]["entry_id"], older["entry_id"])
        self.assertEqual(results[1]["entry_id"], newer["entry_id"])

    def test_date_filters_use_kolkata_calendar_time(self) -> None:
        entry = self.repository.create_entry("note", "Midnight journal")
        with database.get_connection() as connection:
            connection.execute(
                "UPDATE general_entries SET updated_at = ? WHERE entry_id = ?",
                ("2026-07-31 19:00:00", entry["entry_id"]),
            )

        august = self.repository.list_entries(year=2026, month=8)
        july = self.repository.list_entries(year=2026, month=7)

        self.assertEqual(august["total_results"], 1)
        self.assertEqual(july["total_results"], 0)

    def test_date_filters_follow_latest_edit_not_original_date(self) -> None:
        entry = self.repository.create_entry("note", "Living journal")
        with database.get_connection() as connection:
            connection.execute(
                """
                UPDATE general_entries
                SET created_at = ?, updated_at = ?
                WHERE entry_id = ?
                """,
                (
                    "2026-08-02 08:00:00",
                    "2027-01-10 08:00:00",
                    entry["entry_id"],
                ),
            )

        self.assertEqual(
            self.repository.list_entries(year=2027, month=1)["total_results"],
            1,
        )
        self.assertEqual(
            self.repository.list_entries(year=2026, month=8)["total_results"],
            0,
        )

    def test_draft_workflow_creation_filtering_and_publishing(self) -> None:
        published = self.repository.create_entry("note", "Published Note", status="published")
        draft = self.repository.create_entry("note", "Draft Essay", status="draft")

        self.assertEqual(published["status"], "published")
        self.assertEqual(draft["status"], "draft")

        # Default listing only returns published entries
        pub_list = self.repository.list_entries()
        self.assertEqual(pub_list["total_results"], 1)
        self.assertEqual(pub_list["results"][0]["title"], "Published Note")

        # Draft listing returns drafts
        draft_list = self.repository.list_entries(status="draft")
        self.assertEqual(draft_list["total_results"], 1)
        self.assertEqual(draft_list["results"][0]["title"], "Draft Essay")

        # Tags summary includes draft count
        summary = self.repository.get_tags_summary()
        self.assertEqual(summary["draft_entries"], 1)
        self.assertEqual(summary["total_entries"], 1)

        # Publish the draft
        promoted = self.repository.publish_entry(draft["entry_id"])
        self.assertIsNotNone(promoted)
        self.assertEqual(promoted["status"], "published")

        # Now published count is 2
        self.assertEqual(self.repository.list_entries()["total_results"], 2)


if __name__ == "__main__":
    unittest.main()

