from contextlib import closing
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database


class DatabaseBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        root = Path(self.temporary_directory.name)
        self.demo_path = root / "demo.db"
        self.user_path = root / "movie_excluder.db"

    def _patch_paths(self):
        return (
            patch.object(database, "DATABASE_PATH", self.user_path),
            patch.object(database, "DEFAULT_DATABASE_PATH", self.user_path),
            patch.object(database, "DEMO_DATABASE_PATH", self.demo_path),
        )

    def test_demo_database_is_copied_only_when_user_database_is_missing(self) -> None:
        with closing(sqlite3.connect(self.demo_path)) as connection:
            connection.execute("CREATE TABLE demo_marker (value TEXT)")
            connection.execute("INSERT INTO demo_marker VALUES ('sample')")
            connection.commit()

        patches = self._patch_paths()
        with patches[0], patches[1], patches[2]:
            database.ensure_database_exists()
            with closing(sqlite3.connect(self.user_path)) as connection:
                value = connection.execute(
                    "SELECT value FROM demo_marker"
                ).fetchone()[0]
            self.assertEqual(value, "sample")

            with closing(sqlite3.connect(self.user_path)) as connection:
                connection.execute("UPDATE demo_marker SET value = 'personal'")
                connection.commit()
            database.ensure_database_exists()
            with closing(sqlite3.connect(self.user_path)) as connection:
                value = connection.execute(
                    "SELECT value FROM demo_marker"
                ).fetchone()[0]
            self.assertEqual(value, "personal")

    def test_startup_initialization_migrates_the_copied_demo(self) -> None:
        with closing(sqlite3.connect(self.demo_path)) as connection:
            connection.execute(
                "CREATE TABLE movies (tmdb_id INTEGER PRIMARY KEY, title TEXT NOT NULL, fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
            )
            connection.execute("INSERT INTO movies (tmdb_id, title) VALUES (1, 'Demo')")
            connection.commit()

        patches = self._patch_paths()
        with patches[0], patches[1], patches[2]:
            database.initialize_database()
            with database.get_connection() as connection:
                tables = {
                    row["name"]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    ).fetchall()
                }
                movie = connection.execute(
                    "SELECT title FROM movies WHERE tmdb_id = 1"
                ).fetchone()
            self.assertNotIn("looking_out_for", tables)
            self.assertIn("general_entry_tags", tables)
            self.assertEqual(movie["title"], "Demo")


if __name__ == "__main__":
    unittest.main()
