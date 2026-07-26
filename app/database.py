import sqlite3
from pathlib import Path

from app.movie_status import MovieStatus


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "movie_excluder.db"


class DatabaseConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(
        DATABASE_PATH,
        factory=DatabaseConnection,
    )
    connection.row_factory = sqlite3.Row
    return connection


def _create_user_movie_data_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS user_movie_data (
            tmdb_id INTEGER PRIMARY KEY,
            status TEXT NOT NULL DEFAULT '{MovieStatus.NEW_DISCOVERY.value}'
                CHECK (
                    status IN (
                        '{MovieStatus.NEW_DISCOVERY.value}',
                        '{MovieStatus.WATCH_LATER.value}',
                        '{MovieStatus.WATCHED.value}',
                        '{MovieStatus.REWATCH.value}',
                        '{MovieStatus.EXCLUDED.value}'
                    )
                ),
            verdict REAL,
            notes TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tmdb_id) REFERENCES movies (tmdb_id)
        )
        """
    )


def _migrate_legacy_user_movie_data(
    connection: sqlite3.Connection,
) -> None:
    columns = {
        row["name"]
        for row in connection.execute(
            "PRAGMA table_info(user_movie_data)"
        ).fetchall()
    }

    if not columns or "status" in columns:
        return

    legacy_flags = {"watchlist", "watched", "rewatch", "excluded"}

    if not legacy_flags.issubset(columns):
        raise RuntimeError(
            "Unsupported user_movie_data schema. Back up the database "
            "before attempting a manual migration."
        )

    connection.execute(
        "ALTER TABLE user_movie_data RENAME TO user_movie_data_legacy"
    )
    _create_user_movie_data_table(connection)
    connection.execute(
        f"""
        INSERT INTO user_movie_data (
            tmdb_id,
            status,
            verdict,
            notes,
            updated_at
        )
        SELECT
            tmdb_id,
            CASE
                WHEN excluded = 1
                    THEN '{MovieStatus.EXCLUDED.value}'
                WHEN rewatch = 1
                    THEN '{MovieStatus.REWATCH.value}'
                WHEN watched = 1
                    THEN '{MovieStatus.WATCHED.value}'
                WHEN watchlist = 1
                    THEN '{MovieStatus.WATCH_LATER.value}'
                ELSE '{MovieStatus.NEW_DISCOVERY.value}'
            END,
            verdict,
            notes,
            updated_at
        FROM user_movie_data_legacy
        """
    )
    connection.execute("DROP TABLE user_movie_data_legacy")


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                tmdb_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                original_title TEXT,
                release_date TEXT,
                overview TEXT,
                poster_path TEXT,
                backdrop_path TEXT,
                vote_average REAL,
                fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        _migrate_legacy_user_movie_data(connection)
        _create_user_movie_data_table(connection)


if __name__ == "__main__":
    print(f"Using database: {DATABASE_PATH}")
    initialize_database()
