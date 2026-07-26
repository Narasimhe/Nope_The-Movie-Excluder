import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.movie_status import MovieStatus, VALID_MOVIE_STATUSES
from app.user_movie_repository import UserMovieRepository


class PersonalMovieStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        database_path = (
            Path(self.temporary_directory.name)
            / "movie_excluder_test.db"
        )
        database_path_patch = patch.object(
            database,
            "DATABASE_PATH",
            database_path,
        )
        database_path_patch.start()
        self.addCleanup(database_path_patch.stop)

        initialize_database()

        with database.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO movies (tmdb_id, title)
                VALUES (?, ?)
                """,
                (101, "Test Movie"),
            )

        self.repository = UserMovieRepository()

    def test_all_personal_movie_statuses_are_valid(self) -> None:
        for status in sorted(VALID_MOVIE_STATUSES):
            with self.subTest(status=status):
                result = self.repository.set_status(101, status)

                self.assertEqual(result["status"], status)

    def test_invalid_status_is_rejected_without_record(self) -> None:
        with self.assertRaisesRegex(ValueError, "Invalid movie status"):
            self.repository.set_status(101, "maybe_later")

        self.assertIsNone(self.repository.get_user_movie_data(101))

    def test_reversible_changes_preserve_user_content(self) -> None:
        self.repository.set_status(101, MovieStatus.EXCLUDED)
        self.repository.set_notes(101, "Wrong Arrival movie")
        self.repository.set_verdict(101, 2.5)

        self.repository.set_status(101, MovieStatus.NEW_DISCOVERY)
        changed = self.repository.set_status(
            101,
            MovieStatus.WATCH_LATER,
        )

        self.assertEqual(
            changed["status"],
            MovieStatus.WATCH_LATER.value,
        )
        self.assertEqual(changed["notes"], "Wrong Arrival movie")
        self.assertEqual(changed["verdict"], 2.5)

        restored = self.repository.set_status(
            101,
            MovieStatus.EXCLUDED,
        )

        self.assertEqual(
            restored["status"],
            MovieStatus.EXCLUDED.value,
        )
        self.assertEqual(restored["notes"], "Wrong Arrival movie")
        self.assertEqual(restored["verdict"], 2.5)

    def test_notes_create_a_new_discovery_record(self) -> None:
        self.repository.set_notes(101, "Undecided")

        result = self.repository.get_user_movie_data(101)

        self.assertIsNotNone(result)
        self.assertEqual(
            result["status"],
            MovieStatus.NEW_DISCOVERY.value,
        )
        self.assertEqual(result["notes"], "Undecided")

    def test_connection_context_closes_the_database(self) -> None:
        connection = database.get_connection()

        with connection:
            connection.execute("SELECT 1").fetchone()

        with self.assertRaisesRegex(
            sqlite3.ProgrammingError,
            "closed",
        ):
            connection.execute("SELECT 1")

    def test_legacy_flags_are_migrated_safely(self) -> None:
        legacy_path = (
            Path(self.temporary_directory.name)
            / "legacy_movie_excluder.db"
        )

        with closing(sqlite3.connect(legacy_path)) as connection:
            with connection:
                connection.executescript(
                    """
                    CREATE TABLE movies (
                        tmdb_id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        original_title TEXT,
                        release_date TEXT,
                        overview TEXT,
                        poster_path TEXT,
                        backdrop_path TEXT,
                        vote_average REAL,
                        fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE user_movie_data (
                        tmdb_id INTEGER PRIMARY KEY,
                        watchlist INTEGER NOT NULL DEFAULT 0,
                        watched INTEGER NOT NULL DEFAULT 0,
                        rewatch INTEGER NOT NULL DEFAULT 0,
                        excluded INTEGER NOT NULL DEFAULT 0,
                        verdict REAL,
                        notes TEXT,
                        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (tmdb_id) REFERENCES movies (tmdb_id)
                    );

                    INSERT INTO movies (tmdb_id, title)
                    VALUES (101, 'Test Movie');

                    INSERT INTO user_movie_data (
                        tmdb_id,
                        watchlist,
                        watched,
                        rewatch,
                        excluded,
                        verdict,
                        notes
                    )
                    VALUES (
                        101,
                        0,
                        1,
                        0,
                        1,
                        1.5,
                        'Keep this note'
                    );
                    """
                )

        with patch.object(database, "DATABASE_PATH", legacy_path):
            initialize_database()
            result = UserMovieRepository().get_user_movie_data(101)

            self.assertIsNotNone(result)
            self.assertEqual(
                result["status"],
                MovieStatus.EXCLUDED.value,
            )
            self.assertEqual(result["verdict"], 1.5)
            self.assertEqual(result["notes"], "Keep this note")

            with database.get_connection() as connection:
                column_names = {
                    row["name"]
                    for row in connection.execute(
                        "PRAGMA table_info(user_movie_data)"
                    ).fetchall()
                }

        self.assertIn("status", column_names)
        self.assertNotIn("watchlist", column_names)


if __name__ == "__main__":
    unittest.main()
