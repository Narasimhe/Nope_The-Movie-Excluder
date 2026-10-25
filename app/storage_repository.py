import logging
from pathlib import Path
from typing import Any

from app import database
from app.movie_status import MovieStatus

logger = logging.getLogger(__name__)


class StorageRepository:
    def get_summary(self) -> dict[str, Any]:
        with database.get_connection() as connection:
            cached_movies = connection.execute(
                "SELECT COUNT(*) FROM movies"
            ).fetchone()[0]
            personal_movies = connection.execute(
                "SELECT COUNT(*) FROM user_movie_data"
            ).fetchone()[0]
            deleted_entries = connection.execute(
                "SELECT COUNT(*) FROM general_entries WHERE is_deleted = 1"
            ).fetchone()[0]
            cleanup_candidates = connection.execute(
                self._cleanup_candidate_sql(count_only=True),
                ("-90 days",),
            ).fetchone()[0]

        path = Path(database.DATABASE_PATH)
        size_bytes = path.stat().st_size if path.exists() else 0
        return {
            "database_path": str(path),
            "size_bytes": size_bytes,
            "cached_movies": cached_movies,
            "personal_movies": personal_movies,
            "old_unprotected_cache_movies": cleanup_candidates,
            "soft_deleted_entries": deleted_entries,
        }

    def cleanup_old_cache(self, days: int = 90) -> dict[str, Any]:
        if isinstance(days, bool) or not isinstance(days, int) or days < 30:
            raise ValueError("Cache cleanup age must be at least 30 days.")
        with database.get_connection() as connection:
            cursor = connection.execute(
                self._cleanup_candidate_sql(count_only=False),
                (f"-{days} days",),
            )
            removed = cursor.rowcount
            # Prune expired TMDB discover and credit payload caches
            connection.execute(
                "DELETE FROM tmdb_discover_cache WHERE updated_at <= datetime('now', ?)",
                (f"-{days} days",),
            )
            connection.execute(
                "DELETE FROM tmdb_person_credits_cache WHERE updated_at <= datetime('now', ?)",
                (f"-{days} days",),
            )
            connection.execute(
                """
                DELETE FROM movie_country_cache
                WHERE NOT EXISTS (
                    SELECT 1 FROM movies WHERE movies.tmdb_id = movie_country_cache.tmdb_id
                )
                """
            )
            # Storage optimization invariant: NOPE movies never keep bloated metadata
            connection.execute(
                """
                DELETE FROM movie_credits
                WHERE tmdb_id IN (
                    SELECT tmdb_id FROM user_movie_data WHERE status = ?
                )
                """,
                (MovieStatus.EXCLUDED.value,),
            )
            connection.execute(
                """
                DELETE FROM movie_keywords
                WHERE tmdb_id IN (
                    SELECT tmdb_id FROM user_movie_data WHERE status = ?
                )
                AND keyword_id IN (
                    SELECT keyword_id FROM keywords WHERE is_custom = 0
                )
                """,
                (MovieStatus.EXCLUDED.value,),
            )
            connection.execute(
                """
                DELETE FROM keywords
                WHERE NOT EXISTS (
                    SELECT 1 FROM movie_keywords mk
                    WHERE mk.keyword_id = keywords.keyword_id
                )
                """
            )
            connection.execute(
                """
                DELETE FROM genres
                WHERE NOT EXISTS (
                    SELECT 1 FROM movie_genres mg
                    WHERE mg.tmdb_genre_id = genres.tmdb_genre_id
                )
                """
            )
        self._vacuum()
        return {"removed_movies": max(0, removed), "days": days}

    def purge_deleted_entries(self) -> dict[str, int]:
        with database.get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM general_entries WHERE is_deleted = 1"
            )
            removed = cursor.rowcount
            connection.execute(
                """
                DELETE FROM general_entry_tags
                WHERE NOT EXISTS (
                    SELECT 1 FROM general_entry_tag_links links
                    WHERE links.tag_id = general_entry_tags.tag_id
                )
                """
            )
            # Find all banner URLs still in use by active entries
            active_rows = connection.execute(
                "SELECT image_url FROM general_entries WHERE image_url IS NOT NULL AND image_url != ''"
            ).fetchall()
            active_banners = {
                Path(row["image_url"]).name
                for row in active_rows
                if row["image_url"].startswith("/banners/")
            }

        # Automatically clean up orphaned banner files on disk
        banners_dir = Path(__file__).resolve().parent.parent / "data" / "banners"
        if banners_dir.exists():
            for p in banners_dir.iterdir():
                if p.is_file() and p.name not in active_banners:
                    try:
                        p.unlink()
                    except Exception as exc:
                        logger.warning("Could not unlink orphaned banner %s: %s", p, exc)

        self._vacuum()
        return {"removed_entries": max(0, removed)}

    @staticmethod
    def _cleanup_candidate_sql(*, count_only: bool) -> str:
        action = "SELECT COUNT(*) FROM movies m" if count_only else "DELETE FROM movies"
        movie_ref = "m.tmdb_id" if count_only else "movies.tmdb_id"
        accessed_ref = (
            "COALESCE(m.last_accessed_at, m.fetched_at)"
            if count_only
            else "COALESCE(movies.last_accessed_at, movies.fetched_at)"
        )
        return f"""
            {action}
            WHERE {accessed_ref} <= datetime('now', ?)
              AND NOT EXISTS (
                  SELECT 1 FROM user_movie_data u
                  WHERE u.tmdb_id = {movie_ref}
              )
              AND NOT EXISTS (
                  SELECT 1
                  FROM movie_keywords mk
                  JOIN keywords k ON k.keyword_id = mk.keyword_id
                  WHERE mk.tmdb_id = {movie_ref}
                    AND k.is_custom = 1
              )
        """

    @staticmethod
    def _vacuum() -> None:
        with database.get_connection() as connection:
            connection.execute("VACUUM")
