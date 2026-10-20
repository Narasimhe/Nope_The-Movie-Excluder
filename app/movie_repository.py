from typing import Any

from app.database import get_connection
from app.movie_status import MovieStatus, validate_movie_status


class MovieRepository:
    PAGE_SIZE = 20

    def save_movie(self, movie: dict[str, Any]) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO movies (
                    tmdb_id,
                    title,
                    original_title,
                    release_date,
                    overview,
                    poster_path,
                    backdrop_path,
                    vote_average,
                    vote_count,
                    original_language,
                    fetched_at,
                    last_accessed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(tmdb_id) DO UPDATE SET
                    title = excluded.title,
                    original_title = excluded.original_title,
                    release_date = excluded.release_date,
                    overview = excluded.overview,
                    poster_path = excluded.poster_path,
                    backdrop_path = excluded.backdrop_path,
                    vote_average = excluded.vote_average,
                    vote_count = excluded.vote_count,
                    original_language = excluded.original_language,
                    fetched_at = CURRENT_TIMESTAMP,
                    last_accessed_at = CURRENT_TIMESTAMP
                """,
                (
                    movie["id"],
                    movie["title"],
                    movie.get("original_title"),
                    movie.get("release_date"),
                    movie.get("overview"),
                    movie.get("poster_path"),
                    movie.get("backdrop_path"),
                    movie.get("vote_average"),
                    movie.get("vote_count") or 0,
                    movie.get("original_language"),
                ),
            )

    def get_movie(self, tmdb_id: int) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM movies
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            ).fetchone()

        if row is None:
            return None

        return dict(row)

    def touch_movie(self, tmdb_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE movies
                SET last_accessed_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            )

    def get_movies_by_ids(
        self,
        tmdb_ids: list[int],
    ) -> list[dict]:
        unique_ids = list(dict.fromkeys(tmdb_ids))

        if not unique_ids:
            return []

        placeholders = ",".join("?" for _ in unique_ids)

        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT *
                FROM movies
                WHERE tmdb_id IN ({placeholders})
                """,
                unique_ids,
            ).fetchall()

        movies_by_id = {
            row["tmdb_id"]: dict(row)
            for row in rows
        }
        return [
            movies_by_id[tmdb_id]
            for tmdb_id in unique_ids
            if tmdb_id in movies_by_id
        ]

    def search_movies(self, query: str) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM movies
                WHERE title LIKE ?
                   OR original_title LIKE ?
                ORDER BY title
                """,
                (f"%{query}%", f"%{query}%"),
            ).fetchall()

        return [dict(row) for row in rows]

    def search_user_library(
        self,
        query: str = "",
        status: str | None = None,
    ) -> list[dict]:
        cleaned_query = " ".join((query or "").split())
        where_parts: list[str] = []
        params: list[Any] = []

        if cleaned_query:
            escaped_query = (
                cleaned_query.replace("!", "!!")
                .replace("%", "!%")
                .replace("_", "!_")
            )
            like_pattern = f"%{escaped_query}%"
            where_parts.append(
                """(
                    m.title LIKE ? ESCAPE '!' COLLATE NOCASE
                    OR m.original_title LIKE ? ESCAPE '!' COLLATE NOCASE
                    OR m.overview LIKE ? ESCAPE '!' COLLATE NOCASE
                    OR (u.notes IS NOT NULL AND u.notes LIKE ? ESCAPE '!' COLLATE NOCASE)
                    OR EXISTS (
                        SELECT 1 FROM movie_keywords mk
                        JOIN keywords k ON mk.keyword_id = k.keyword_id
                        WHERE mk.tmdb_id = m.tmdb_id
                          AND k.name LIKE ? ESCAPE '!' COLLATE NOCASE
                    )
                )"""
            )
            params.extend([like_pattern, like_pattern, like_pattern, like_pattern, like_pattern])

        if status:
            if status == "favorites":
                where_parts.append("u.is_favorite = 1 AND u.status IN ('watched', 'rewatch')")
            elif status == "movie-notes":
                where_parts.append("u.notes IS NOT NULL AND TRIM(u.notes) <> ''")
            elif status == "watched":
                where_parts.append("u.status IN ('watched', 'rewatch')")
            elif status == "new_discovery":
                where_parts.append("u.status = 'new_discovery' AND NOT EXISTS (SELECT 1 FROM looking_out_for l WHERE l.tmdb_id = m.tmdb_id)")
            else:
                target_status = "excluded" if status == "nope" else status
                validated_status = validate_movie_status(target_status)
                where_parts.append("u.status = ?")
                params.append(validated_status)
        else:
            where_parts.append("(u.status IS NOT NULL OR u.is_favorite = 1 OR (u.notes IS NOT NULL AND TRIM(u.notes) <> ''))")

        where_clause = " AND ".join(where_parts)

        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                WHERE {where_clause}
                ORDER BY m.title COLLATE NOCASE
                """,
                tuple(params),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_watched_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status IN (?, ?)
                ORDER BY m.title
                """,
                (
                    MovieStatus.WATCHED.value,
                    MovieStatus.REWATCH.value,
                ),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_watchlist_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                  AND NOT EXISTS (
                      SELECT 1
                      FROM looking_out_for l
                      WHERE l.tmdb_id = m.tmdb_id
                  )
                ORDER BY m.title
                """,
                (MovieStatus.WATCH_LATER.value,),
            ).fetchall()

        return [dict(row) for row in rows]
    
    def get_rewatch_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                ORDER BY m.title
                """,
                (MovieStatus.REWATCH.value,),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_excluded_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                ORDER BY m.title
                """,
                (MovieStatus.EXCLUDED.value,),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_favorite_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.is_favorite = 1
                  AND u.status IN (?, ?)
                ORDER BY m.title
                """,
                (
                    MovieStatus.WATCHED.value,
                    MovieStatus.REWATCH.value,
                ),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_new_discovery_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                ORDER BY m.title
                """,
                (MovieStatus.NEW_DISCOVERY.value,),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_movies_by_status(
        self,
        status: str | MovieStatus,
    ) -> list[dict]:
        validated_status = validate_movie_status(status)

        looking_out_clause = (
            " AND NOT EXISTS ("
            "SELECT 1 FROM looking_out_for l "
            "WHERE l.tmdb_id = m.tmdb_id)"
            if validated_status == MovieStatus.NEW_DISCOVERY.value
            else ""
        )

        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                {looking_out_clause}
                ORDER BY m.title
                """,
                (validated_status,),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_movies_by_status_page(
        self,
        status: str | MovieStatus,
        page: int = 1,
        page_size: int = PAGE_SIZE,
    ) -> dict:
        validated_status = validate_movie_status(status)
        where_clause = "u.status = ?"
        if validated_status == MovieStatus.NEW_DISCOVERY.value:
            where_clause += (
                " AND NOT EXISTS ("
                "SELECT 1 FROM looking_out_for l "
                "WHERE l.tmdb_id = m.tmdb_id)"
            )
        return self._get_user_movie_page(
            where_clause,
            (validated_status,),
            page,
            page_size=page_size,
        )

    def get_watched_movies_page(self, page: int = 1, page_size: int = PAGE_SIZE) -> dict:
        return self._get_user_movie_page(
            "u.status IN (?, ?)",
            (MovieStatus.WATCHED.value, MovieStatus.REWATCH.value),
            page,
            page_size=page_size,
        )

    def get_favorite_movies_page(self, page: int = 1, page_size: int = PAGE_SIZE) -> dict:
        return self._get_user_movie_page(
            "u.is_favorite = 1 AND u.status IN (?, ?)",
            (MovieStatus.WATCHED.value, MovieStatus.REWATCH.value),
            page,
            page_size=page_size,
        )

    def get_movies_with_notes_page(self, page: int = 1, page_size: int = PAGE_SIZE) -> dict:
        return self._get_user_movie_page(
            "u.notes IS NOT NULL AND TRIM(u.notes) <> ''",
            (),
            page,
            page_size=page_size,
        )

    def _get_user_movie_page(
        self,
        where_clause: str,
        parameters: tuple,
        page: int,
        page_size: int = PAGE_SIZE,
    ) -> dict:
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValueError("Movie page must be at least 1.")
        if isinstance(page_size, bool) or not isinstance(page_size, int) or page_size < 1:
            page_size = self.PAGE_SIZE
        offset = (page - 1) * page_size
        with get_connection() as connection:
            total = connection.execute(
                f"""
                SELECT COUNT(*)
                FROM movies m
                JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                WHERE {where_clause}
                """,
                parameters,
            ).fetchone()[0]
            rows = connection.execute(
                f"""
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                WHERE {where_clause}
                ORDER BY m.title COLLATE NOCASE, m.tmdb_id
                LIMIT ? OFFSET ?
                """,
                (*parameters, page_size, offset),
            ).fetchall()
        return {
            "page": page,
            "page_size": page_size,
            "total_results": total,
            "total_pages": max(1, (total + page_size - 1) // page_size),
            "results": [dict(row) for row in rows],
        }

    def mark_metadata_fetched(self, tmdb_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE movies
                SET metadata_fetched_at = CURRENT_TIMESTAMP,
                    metadata_version = 2
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            )
