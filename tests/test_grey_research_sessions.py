import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.grey_service import GreyService


class GreyResearchFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        self.research_dir = Path(self.temporary_directory.name) / "research"
        self.research_dir.mkdir(parents=True, exist_ok=True)

        database_path = Path(self.temporary_directory.name) / "test_research.db"
        database_path_patch = patch.object(
            database,
            "DATABASE_PATH",
            database_path,
        )
        database_path_patch.start()
        self.addCleanup(database_path_patch.stop)

        initialize_database()
        self.service = GreyService(db_path=str(database_path))
        self.service.research_dir = self.research_dir

    def test_research_files_index_empty(self) -> None:
        index_str = self.service.get_research_files_index()
        self.assertIn("No research files", index_str)

    def test_save_and_auto_index_research_file(self) -> None:
        file_path = self.research_dir / "high_frequency_title_words.md"
        file_path.write_text("# High Frequency Words\n\n- Night\n- World\n", encoding="utf-8")

        index_str = self.service.get_research_files_index()
        self.assertIn("high_frequency_title_words.md", index_str)

    def test_resolve_research_file_exact_and_fuzzy(self) -> None:
        file_path = self.research_dir / "70s_neo_noir_dig.md"
        file_path.write_text("# 70s Neo Noir\n", encoding="utf-8")

        resolved_exact = self.service.resolve_research_file("70s_neo_noir_dig.md")
        self.assertIsNotNone(resolved_exact)
        self.assertEqual(resolved_exact.name, "70s_neo_noir_dig.md")

        resolved_fuzzy = self.service.resolve_research_file("70s neo noir")
        self.assertIsNotNone(resolved_fuzzy)
        self.assertEqual(resolved_fuzzy.name, "70s_neo_noir_dig.md")

    def test_append_research_file(self) -> None:
        file_path = self.research_dir / "high_frequency_words.md"
        file_path.write_text("# High Frequency Words\n", encoding="utf-8")

        # Emulate action execution logic for append_research_file
        matched = self.service.resolve_research_file("high frequency")
        self.assertIsNotNone(matched)
        with open(matched, "a", encoding="utf-8") as af:
            af.write("- **Far**: *Far from Heaven (2002)*\n")

        content = file_path.read_text(encoding="utf-8")
        self.assertIn("Far from Heaven", content)

    def test_auto_index_reflects_external_file_deletion(self) -> None:
        file_path = self.research_dir / "scandi_thrillers.md"
        file_path.write_text("# Scandi Thrillers\n", encoding="utf-8")
        self.assertIn("scandi_thrillers.md", self.service.get_research_files_index())

        # Simulate user deleting file in VS Code / File Explorer
        file_path.unlink()

        # Next check immediately reflects deletion without any sync
        self.assertNotIn("scandi_thrillers.md", self.service.get_research_files_index())

    def test_grey_service_research_skill_routing(self) -> None:
        with patch.object(self.service, "_get_connection", side_effect=database.get_connection):
            res = self.service.chat(
                message="/research",
                current_view="library",
            )
            self.assertEqual(res.get("active_skill"), "research")
            self.assertEqual(res.get("active_skill_name"), "Cinema Research Files")
