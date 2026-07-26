from typing import Any

from app.database import get_connection
from app.movie_status import MovieStatus, validate_movie_status


class MovieRepository:
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
                    fetched_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(tmdb_id) DO UPDATE SET
                    title = excluded.title,
                    original_title = excluded.original_title,
                    release_date = excluded.release_date,
                    overview = excluded.overview,
                    poster_path = excluded.poster_path,
                    backdrop_path = excluded.backdrop_path,
                    vote_average = excluded.vote_average,
                    fetched_at = CURRENT_TIMESTAMP
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
                (validated_status,),
            ).fetchall()

        return [dict(row) for row in rows]

    def mark_metadata_fetched(self, tmdb_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE movies
                SET metadata_fetched_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            )
