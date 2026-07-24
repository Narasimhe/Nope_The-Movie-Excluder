import sqlite3
from pathlib import Path

DATABASE_PATH = Path("movie_excluder.db")


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
                watched INTEGER NOT NULL DEFAULT 0,
                blacklisted INTEGER NOT NULL DEFAULT 0,
                watchlisted INTEGER NOT NULL DEFAULT 0,
                personal_rating REAL,
                review TEXT,
                notes TEXT,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tmdb_id) REFERENCES movies (tmdb_id)
            );
            """
        )