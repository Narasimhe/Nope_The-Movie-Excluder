import sqlite3
from typing import Any

from app.database import get_connection


class UserMovieRepository:
    def _ensure_record(self, tmdb_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO user_movie_data (tmdb_id)
                VALUES (?)
                ON CONFLICT(tmdb_id) DO NOTHING
                """,
                (tmdb_id,),
            )

    def set_watchlist(self, tmdb_id: int, value: bool) -> None:
        self._ensure_record(tmdb_id)

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE user_movie_data
                SET watchlist = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (int(value), tmdb_id),
            )

    def set_watched(self, tmdb_id: int, value: bool) -> None:
        self._ensure_record(tmdb_id)

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE user_movie_data
                SET watched = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (int(value), tmdb_id),
            )

    def set_rewatch(self, tmdb_id: int, value: bool) -> None:
        self._ensure_record(tmdb_id)

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE user_movie_data
                SET rewatch = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (int(value), tmdb_id),
            )

    def set_excluded(self, tmdb_id: int, value: bool) -> None:
        self._ensure_record(tmdb_id)

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE user_movie_data
                SET excluded = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (int(value), tmdb_id),
            )

    def set_verdict(self, tmdb_id: int, verdict: float | None) -> None:
        self._ensure_record(tmdb_id)

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE user_movie_data
                SET verdict = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (verdict, tmdb_id),
            )

    def set_notes(self, tmdb_id: int, notes: str | None) -> None:
        self._ensure_record(tmdb_id)

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE user_movie_data
                SET notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (notes, tmdb_id),
            )

    def get_user_movie_data(
        self,
        tmdb_id: int,
    ) -> dict[str, Any] | None:
        with get_connection() as connection:
            connection.row_factory = sqlite3.Row

            row = connection.execute(
                """
                SELECT
                    tmdb_id,
                    watchlist,
                    watched,
                    rewatch,
                    excluded,
                    verdict,
                    notes,
                    updated_at
                FROM user_movie_data
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            ).fetchone()

        if row is None:
            return None

        result = dict(row)

        for field in ("watchlist", "watched", "rewatch", "excluded"):
            result[field] = bool(result[field])

        return result

    def get_watched_movie_ids(self) -> set[int]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT tmdb_id
                FROM user_movie_data
                WHERE watched = 1
                """
            ).fetchall()

        return {row[0] for row in rows}

    def get_excluded_movie_ids(self) -> set[int]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT tmdb_id
                FROM user_movie_data
                WHERE excluded = 1
                """
            ).fetchall()

        return {row[0] for row in rows}