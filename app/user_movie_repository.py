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
                    is_favorite = CASE
                        WHEN excluded.status IN (?, ?)
                            THEN user_movie_data.is_favorite
                        ELSE 0
                    END,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    tmdb_id,
                    validated_status,
                    MovieStatus.WATCHED.value,
                    MovieStatus.REWATCH.value,
                ),
            )

        result = self.get_user_movie_data(tmdb_id)

        if result is None:
            raise RuntimeError(
                f"Could not read personal data for TMDB movie {tmdb_id}."
            )

        return result

    def remove_status(self, tmdb_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                "DELETE FROM user_movie_data WHERE tmdb_id = ?",
                (tmdb_id,),
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

    def set_favorite(
        self,
        tmdb_id: int,
        is_favorite: bool,
    ) -> dict[str, Any]:
        if not isinstance(is_favorite, bool):
            raise ValueError("is_favorite must be true or false.")

        existing = self.get_user_movie_data(tmdb_id)

        if existing is None:
            raise ValueError(
                "Only watched or rewatch movies can be favorited."
            )

        if existing["status"] not in {
            MovieStatus.WATCHED.value,
            MovieStatus.REWATCH.value,
        }:
            raise ValueError(
                "Only watched or rewatch movies can be favorited."
            )

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE user_movie_data
                SET
                    is_favorite = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (int(is_favorite), tmdb_id),
            )

        result = self.get_user_movie_data(tmdb_id)

        if result is None:
            raise RuntimeError(
                "Favorite status was saved but could not be read."
            )

        return result

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
                    is_favorite,
                    updated_at
                FROM user_movie_data
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            ).fetchone()

        if row is None:
            return None

        result = dict(row)
        result["is_favorite"] = bool(result["is_favorite"])
        return result

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
            columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(user_movie_data)"
                ).fetchall()
            }
            favorite_expression = (
                "is_favorite"
                if "is_favorite" in columns
                else "0 AS is_favorite"
            )
            rows = connection.execute(
                f"""
                SELECT
                    tmdb_id,
                    status,
                    verdict,
                    notes,
                    {favorite_expression},
                    updated_at
                FROM user_movie_data
                WHERE tmdb_id IN ({placeholders})
                """,
                tmdb_ids,
            ).fetchall()

        results: dict[int, dict[str, Any]] = {}

        for row in rows:
            movie_data = dict(row)
            movie_data["is_favorite"] = bool(
                movie_data["is_favorite"]
            )
            results[movie_data["tmdb_id"]] = movie_data

        return results

    def search_notes(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        if not isinstance(query, str):
            raise ValueError("Notes search query must be text.")

        raw_terms = [t.strip() for t in query.split(",") if t.strip()]
        if not raw_terms:
            raise ValueError("Notes search query cannot be empty.")

        conditions = []
        params = []
        for term in raw_terms:
            cleaned_term = " ".join(term.split())
            if not cleaned_term:
                continue
            escaped_term = (
                cleaned_term
                .replace("!", "!!")
                .replace("%", "!%")
                .replace("_", "!_")
            )
            conditions.append(
                """(
                    u.notes LIKE ? ESCAPE '!' COLLATE NOCASE
                    OR m.title LIKE ? ESCAPE '!' COLLATE NOCASE
                    OR EXISTS (
                        SELECT 1
                        FROM movie_genres mg
                        JOIN genres g ON mg.tmdb_genre_id = g.tmdb_genre_id
                        WHERE mg.tmdb_id = u.tmdb_id
                          AND g.name LIKE ? ESCAPE '!' COLLATE NOCASE
                    )
                )"""
            )
            term_wildcard = f"%{escaped_term}%"
            params.extend([term_wildcard, term_wildcard, term_wildcard])

        if not conditions:
            raise ValueError("Notes search query cannot be empty.")

        sql = f"""
            SELECT
                u.tmdb_id,
                u.status,
                u.verdict,
                u.notes,
                u.is_favorite,
                u.updated_at
            FROM user_movie_data u
            JOIN movies m ON u.tmdb_id = m.tmdb_id
            WHERE u.notes IS NOT NULL
              AND TRIM(u.notes) <> ''
              AND {" AND ".join(conditions)}
            ORDER BY u.updated_at DESC, u.tmdb_id
        """

        with get_connection() as connection:
            rows = connection.execute(sql, tuple(params)).fetchall()

        results = []

        for row in rows:
            result = dict(row)
            result["is_favorite"] = bool(result["is_favorite"])
            results.append(result)

        return results
