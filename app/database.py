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


def _create_movie_metadata_tables(
    connection: sqlite3.Connection,
) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS genres (
            tmdb_genre_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS movie_genres (
            tmdb_id INTEGER NOT NULL,
            tmdb_genre_id INTEGER NOT NULL,
            PRIMARY KEY (tmdb_id, tmdb_genre_id),
            FOREIGN KEY (tmdb_id)
                REFERENCES movies (tmdb_id)
                ON DELETE CASCADE,
            FOREIGN KEY (tmdb_genre_id)
                REFERENCES genres (tmdb_genre_id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS keywords (
            keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_keyword_id INTEGER UNIQUE,
            name TEXT NOT NULL COLLATE NOCASE,
            is_custom INTEGER NOT NULL
                CHECK (is_custom IN (0, 1)),
            CHECK (
                (is_custom = 0 AND tmdb_keyword_id IS NOT NULL)
                OR
                (is_custom = 1 AND tmdb_keyword_id IS NULL)
            )
        );

        CREATE UNIQUE INDEX IF NOT EXISTS
            idx_unique_custom_keyword_name
        ON keywords (name COLLATE NOCASE)
        WHERE is_custom = 1;

        CREATE TABLE IF NOT EXISTS movie_keywords (
            tmdb_id INTEGER NOT NULL,
            keyword_id INTEGER NOT NULL,
            position INTEGER
                CHECK (
                    position IS NULL
                    OR position BETWEEN 1 AND 5
                ),
            PRIMARY KEY (tmdb_id, keyword_id),
            FOREIGN KEY (tmdb_id)
                REFERENCES movies (tmdb_id)
                ON DELETE CASCADE,
            FOREIGN KEY (keyword_id)
                REFERENCES keywords (keyword_id)
                ON DELETE CASCADE
        );

        CREATE UNIQUE INDEX IF NOT EXISTS
            idx_unique_official_keyword_position
        ON movie_keywords (tmdb_id, position)
        WHERE position IS NOT NULL;
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
                fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                metadata_fetched_at TEXT
            )
            """
        )
        movie_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(movies)"
            ).fetchall()
        }

        if "metadata_fetched_at" not in movie_columns:
            connection.execute(
                """
                ALTER TABLE movies
                ADD COLUMN metadata_fetched_at TEXT
                """
            )

        _migrate_legacy_user_movie_data(connection)
        _create_user_movie_data_table(connection)
        _create_movie_metadata_tables(connection)


if __name__ == "__main__":
    print(f"Using database: {DATABASE_PATH}")
    initialize_database()
