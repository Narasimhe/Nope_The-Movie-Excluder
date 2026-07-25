import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "movie_excluder.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.executescript(
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
            );

           CREATE TABLE IF NOT EXISTS user_movie_data (
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
            """
        )


if __name__ == "__main__":
    print(f"Using database: {DATABASE_PATH}")
    initialize_database()