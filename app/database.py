import shutil
import sqlite3
from pathlib import Path

from app.movie_status import MovieStatus


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "movie_excluder.db"
PRODUCTION_DATABASE_PATH = DATABASE_PATH
DEFAULT_DATABASE_PATH = DATABASE_PATH
DEMO_DATABASE_PATH = DATA_DIR / "demo.db"


def ensure_database_exists() -> None:
    """Create the working database from the demo template only once."""
    if DATABASE_PATH.exists():
        return

    # Tests and diagnostic tools replace DATABASE_PATH with a temporary file.
    # Demo bootstrapping belongs only to the application's configured database.
    if DATABASE_PATH == DEFAULT_DATABASE_PATH and DEMO_DATABASE_PATH.exists():
        shutil.copyfile(DEMO_DATABASE_PATH, DATABASE_PATH)


class DatabaseConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def get_connection() -> sqlite3.Connection:
    import sys
    if "pytest" in sys.modules and DATABASE_PATH == PRODUCTION_DATABASE_PATH:
        raise RuntimeError(
            "SAFETY VIOLATION: Tests must never connect to live production DATABASE_PATH. "
            "Use an isolated temporary test database."
        )
    ensure_database_exists()
    connection = sqlite3.connect(
        DATABASE_PATH,
        factory=DatabaseConnection,
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
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
            is_favorite INTEGER NOT NULL DEFAULT 0
                CHECK (is_favorite IN (0, 1))
                CHECK (
                    is_favorite = 0
                    OR status IN (
                        '{MovieStatus.WATCHED.value}',
                        '{MovieStatus.REWATCH.value}'
                    )
                ),
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tmdb_id) REFERENCES movies (tmdb_id)
        )
        """
    )


def _ensure_user_movie_favorite_column(
    connection: sqlite3.Connection,
) -> None:
    columns = {
        row["name"]
        for row in connection.execute(
            "PRAGMA table_info(user_movie_data)"
        ).fetchall()
    }

    if "is_favorite" not in columns:
        connection.execute(
            f"""
            ALTER TABLE user_movie_data
            ADD COLUMN is_favorite INTEGER NOT NULL DEFAULT 0
                CHECK (is_favorite IN (0, 1))
                CHECK (
                    is_favorite = 0
                    OR status IN (
                        '{MovieStatus.WATCHED.value}',
                        '{MovieStatus.REWATCH.value}'
                    )
                )
            """
        )

    connection.execute(
        """
        UPDATE user_movie_data
        SET is_favorite = 0
        WHERE is_favorite = 1
          AND status NOT IN (?, ?)
        """,
        (
            MovieStatus.WATCHED.value,
            MovieStatus.REWATCH.value,
        ),
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_user_movie_favorites
        ON user_movie_data (is_favorite)
        WHERE is_favorite = 1
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
                    OR position BETWEEN 1 AND 10
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

        CREATE TABLE IF NOT EXISTS movie_credits (
            tmdb_id INTEGER NOT NULL,
            tmdb_person_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            credit_type TEXT NOT NULL
                CHECK (credit_type IN ('director', 'actor')),
            character_name TEXT,
            position INTEGER NOT NULL,
            PRIMARY KEY (tmdb_id, tmdb_person_id, credit_type),
            FOREIGN KEY (tmdb_id)
                REFERENCES movies (tmdb_id)
                ON DELETE CASCADE
        );
        """
    )

    table_row = connection.execute(
        """
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table'
          AND name = 'movie_keywords'
        """
    ).fetchone()

    table_sql = str(table_row["sql"] or "") if table_row else ""

    if "BETWEEN 1 AND 5" in table_sql:
        connection.execute(
            "DROP INDEX IF EXISTS idx_unique_official_keyword_position"
        )
        connection.execute(
            "ALTER TABLE movie_keywords RENAME TO movie_keywords_legacy"
        )
        connection.execute(
            """
            CREATE TABLE movie_keywords (
                tmdb_id INTEGER NOT NULL,
                keyword_id INTEGER NOT NULL,
                position INTEGER
                    CHECK (
                        position IS NULL
                        OR position BETWEEN 1 AND 10
                    ),
                PRIMARY KEY (tmdb_id, keyword_id),
                FOREIGN KEY (tmdb_id) REFERENCES movies (tmdb_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (keyword_id) REFERENCES keywords (keyword_id)
                    ON DELETE CASCADE
            )
            """
        )
        connection.execute(
            """
            INSERT INTO movie_keywords (tmdb_id, keyword_id, position)
            SELECT tmdb_id, keyword_id, position
            FROM movie_keywords_legacy
            """
        )
        connection.execute("DROP TABLE movie_keywords_legacy")
        connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_unique_official_keyword_position
            ON movie_keywords (tmdb_id, position)
            WHERE position IS NOT NULL
            """
        )


def _create_search_preferences_table(
    connection: sqlite3.Connection,
) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS search_preferences (
            preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL COLLATE NOCASE UNIQUE,
            filters_json TEXT NOT NULL,
            personal_filters_json TEXT NOT NULL DEFAULT '{}',
            is_default INTEGER NOT NULL DEFAULT 0
                CHECK (is_default IN (0, 1)),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE UNIQUE INDEX IF NOT EXISTS
            idx_single_default_search_preference
        ON search_preferences (is_default)
        WHERE is_default = 1;
        """
    )

    columns = {
        row["name"]
        for row in connection.execute(
            "PRAGMA table_info(search_preferences)"
        ).fetchall()
    }

    if "personal_filters_json" not in columns:
        connection.execute(
            """
            ALTER TABLE search_preferences
            ADD COLUMN personal_filters_json TEXT NOT NULL DEFAULT '{}'
            """
        )


def _create_search_state_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS search_state (
            state_id INTEGER PRIMARY KEY CHECK (state_id = 1),
            mode TEXT NOT NULL DEFAULT 'simple'
                CHECK (mode IN ('simple', 'advanced', 'super')),
            filters_json TEXT NOT NULL DEFAULT '{}',
            personal_filters_json TEXT NOT NULL DEFAULT '{}',
            selected_preference_id INTEGER,
            filters_collapsed INTEGER NOT NULL DEFAULT 0
                CHECK (filters_collapsed IN (0, 1)),
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def _create_general_entries_table(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS general_entries (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_type TEXT NOT NULL
                CHECK (entry_type IN ('note', 'link')),
            title TEXT NOT NULL,
            body TEXT,
            url TEXT,
            is_deleted INTEGER NOT NULL DEFAULT 0
                CHECK (is_deleted IN (0, 1)),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_general_entries_recent
        ON general_entries (is_deleted, updated_at DESC, entry_id DESC);

        CREATE TABLE IF NOT EXISTS general_entry_tags (
            tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL COLLATE NOCASE UNIQUE
        );

        CREATE TABLE IF NOT EXISTS general_entry_tag_links (
            entry_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (entry_id, tag_id),
            FOREIGN KEY (entry_id)
                REFERENCES general_entries (entry_id)
                ON DELETE CASCADE,
            FOREIGN KEY (tag_id)
                REFERENCES general_entry_tags (tag_id)
                ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_general_entry_tag_links_tag
        ON general_entry_tag_links (tag_id, entry_id);
        """
    )
    entry_cols = {
        row[1]
        for row in connection.execute("PRAGMA table_info(general_entries)").fetchall()
    }
    if "is_pinned" not in entry_cols:
        connection.execute(
            "ALTER TABLE general_entries ADD COLUMN is_pinned INTEGER NOT NULL DEFAULT 0 CHECK (is_pinned IN (0, 1))"
        )
    if "is_archived" not in entry_cols:
        connection.execute(
            "ALTER TABLE general_entries ADD COLUMN is_archived INTEGER NOT NULL DEFAULT 0 CHECK (is_archived IN (0, 1))"
        )
    if "status" not in entry_cols:
        connection.execute(
            "ALTER TABLE general_entries ADD COLUMN status TEXT NOT NULL DEFAULT 'published' CHECK (status IN ('published', 'draft'))"
        )
    if "image_url" not in entry_cols:
        connection.execute(
            "ALTER TABLE general_entries ADD COLUMN image_url TEXT"
        )
    connection.executescript(
        """
        CREATE INDEX IF NOT EXISTS idx_general_entries_pinned_archived
        ON general_entries (is_deleted, is_archived, is_pinned DESC, updated_at DESC);

        CREATE INDEX IF NOT EXISTS idx_general_entries_status
        ON general_entries (is_deleted, status, is_archived, updated_at DESC);
        """
    )


def _ensure_movie_cache_columns(
    connection: sqlite3.Connection,
    movie_columns: set[str],
) -> None:
    if "last_accessed_at" not in movie_columns:
        connection.execute(
            """
            ALTER TABLE movies
            ADD COLUMN last_accessed_at TEXT
            """
        )
        connection.execute(
            """
            UPDATE movies
            SET last_accessed_at = COALESCE(fetched_at, CURRENT_TIMESTAMP)
            WHERE last_accessed_at IS NULL
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
                vote_count INTEGER DEFAULT 0,
                original_language TEXT,
                fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                metadata_fetched_at TEXT,
                metadata_version INTEGER NOT NULL DEFAULT 2,
                last_accessed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        movie_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(movies)"
            ).fetchall()
        }

        if "vote_count" not in movie_columns:
            connection.execute(
                """
                ALTER TABLE movies
                ADD COLUMN vote_count INTEGER DEFAULT 0
                """
            )

        if "metadata_fetched_at" not in movie_columns:
            connection.execute(
                """
                ALTER TABLE movies
                ADD COLUMN metadata_fetched_at TEXT
                """
            )

        if "original_language" not in movie_columns:
            connection.execute(
                """
                ALTER TABLE movies
                ADD COLUMN original_language TEXT
                """
            )

        if "metadata_version" not in movie_columns:
            connection.execute(
                """
                ALTER TABLE movies
                ADD COLUMN metadata_version INTEGER NOT NULL DEFAULT 1
                """
            )

        _ensure_movie_cache_columns(connection, movie_columns)

        connection.execute(
            """
            UPDATE movies
            SET original_language = 'en'
            WHERE original_language IS NOT NULL
              AND (original_language LIKE '2026%' OR LENGTH(original_language) > 10)
            """
        )

        _migrate_legacy_user_movie_data(connection)
        _create_user_movie_data_table(connection)
        _ensure_user_movie_favorite_column(connection)
        _create_movie_metadata_tables(connection)
        _create_search_preferences_table(connection)
        _create_search_state_table(connection)
        _create_general_entries_table(connection)
        connection.executescript(
            """
            DROP INDEX IF EXISTS idx_looking_out_for_release;
            DROP TABLE IF EXISTS looking_out_for;

            CREATE TABLE IF NOT EXISTS movie_country_cache (
                tmdb_id INTEGER PRIMARY KEY,
                origin_country TEXT,
                production_countries TEXT,
                fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS tmdb_discover_cache (
                cache_key TEXT PRIMARY KEY,
                response_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_tmdb_discover_cache_updated
            ON tmdb_discover_cache (updated_at);

            CREATE TABLE IF NOT EXISTS tmdb_person_credits_cache (
                person_id INTEGER PRIMARY KEY,
                response_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )


if __name__ == "__main__":
    print(f"Using database: {DATABASE_PATH}")
    initialize_database()
