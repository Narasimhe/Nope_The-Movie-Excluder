import sqlite3
from typing import Any

from app.database import get_connection
from app.movie_status import MovieStatus, validate_movie_status


class UserMovieRepository:
    def _ensure_record(self, tmdb_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO user_movie_data (tmdb_id, status)
                VALUES (?, ?)
                ON CONFLICT(tmdb_id) DO NOTHING
                """,
                (tmdb_id, MovieStatus.NEW_DISCOVERY.value),
            )

    def set_status(
        self,
        tmdb_id: int,
        status: str | MovieStatus,
    ) -> dict[str, Any]:
        validated_status = validate_movie_status(status)
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO user_movie_data (tmdb_id, status)
                VALUES (?, ?)
                ON CONFLICT(tmdb_id) DO UPDATE SET
                    status = excluded.status,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (tmdb_id, validated_status),
            )

        result = self.get_user_movie_data(tmdb_id)

        if result is None:
            raise RuntimeError(
                f"Could not read personal data for TMDB movie {tmdb_id}."
            )

        return result

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
                    status,
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

        return dict(row)

    def get_watched_movie_ids(self) -> set[int]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT tmdb_id
                FROM user_movie_data
                WHERE status IN (?, ?)
                """,
                (
                    MovieStatus.WATCHED.value,
                    MovieStatus.REWATCH.value,
                ),
            ).fetchall()

        return {row[0] for row in rows}

    def get_excluded_movie_ids(self) -> set[int]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT tmdb_id
                FROM user_movie_data
                WHERE status = ?
                """,
                (MovieStatus.EXCLUDED.value,),
            ).fetchall()

        return {row[0] for row in rows}

    def get_user_movie_data_bulk(
        self,
        tmdb_ids: list[int],
    ) -> dict[int, dict[str, Any]]:
        if not tmdb_ids:
            return {}

        placeholders = ",".join("?" for _ in tmdb_ids)

        with get_connection() as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                f"""
                SELECT
                    tmdb_id,
                    status,
                    verdict,
                    notes,
                    updated_at
                FROM user_movie_data
                WHERE tmdb_id IN ({placeholders})
                """,
                tmdb_ids,
            ).fetchall()

        results: dict[int, dict[str, Any]] = {}

        for row in rows:
            movie_data = dict(row)
            results[movie_data["tmdb_id"]] = movie_data

        return results
