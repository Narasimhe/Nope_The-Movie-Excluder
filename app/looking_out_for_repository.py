from typing import Any

from app.database import get_connection


class LookingOutForRepository:
    PAGE_SIZE = 20

    def add(self, tmdb_id: int, release_date: str) -> dict[str, Any]:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO looking_out_for (tmdb_id, release_date)
                VALUES (?, ?)
                ON CONFLICT(tmdb_id) DO UPDATE SET
                    release_date = excluded.release_date,
                    last_checked_at = CURRENT_TIMESTAMP
                """,
                (tmdb_id, release_date),
            )
        result = self.get(tmdb_id)
        if result is None:
            raise RuntimeError("Upcoming movie was saved but could not be read.")
        return result

    def get(self, tmdb_id: int) -> dict[str, Any] | None:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT tmdb_id, release_date, tracked_at, last_checked_at
                FROM looking_out_for
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            ).fetchone()
        return dict(row) if row is not None else None

    def remove(self, tmdb_id: int) -> bool:
        with get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM looking_out_for WHERE tmdb_id = ?",
                (tmdb_id,),
            )
        return cursor.rowcount > 0

    def update_release_date(self, tmdb_id: int, release_date: str) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE looking_out_for
                SET release_date = ?,
                    last_checked_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (release_date, tmdb_id),
            )

    def mark_checked(self, tmdb_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE looking_out_for
                SET last_checked_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            )

    def get_stale_movie_ids(self, hours: int = 24) -> list[int]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT tmdb_id
                FROM looking_out_for
                WHERE last_checked_at <= datetime('now', ?)
                ORDER BY last_checked_at, tmdb_id
                LIMIT 50
                """,
                (f"-{hours} hours",),
            ).fetchall()
        return [int(row["tmdb_id"]) for row in rows]

    def list_page(
        self,
        page: int = 1,
        today: str | None = None,
    ) -> dict[str, Any]:
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValueError("Looking Out For page must be at least 1.")
        offset = (page - 1) * self.PAGE_SIZE
        with get_connection() as connection:
            total = connection.execute(
                "SELECT COUNT(*) FROM looking_out_for"
            ).fetchone()[0]
            rows = connection.execute(
                """
                SELECT
                    m.*,
                    l.release_date AS looking_out_release_date,
                    l.tracked_at,
                    l.last_checked_at
                FROM looking_out_for l
                JOIN movies m ON m.tmdb_id = l.tmdb_id
                ORDER BY
                    CASE
                        WHEN ? IS NULL OR l.release_date >= ? THEN 0
                        ELSE 1
                    END,
                    CASE
                        WHEN ? IS NULL OR l.release_date >= ?
                            THEN l.release_date
                    END ASC,
                    CASE
                        WHEN ? IS NOT NULL AND l.release_date < ?
                            THEN l.release_date
                    END DESC,
                    m.title COLLATE NOCASE,
                    m.tmdb_id
                LIMIT ? OFFSET ?
                """,
                (
                    today, today,
                    today, today,
                    today, today,
                    self.PAGE_SIZE, offset,
                ),
            ).fetchall()
        return {
            "page": page,
            "page_size": self.PAGE_SIZE,
            "total_results": total,
            "total_pages": max(1, (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE),
            "results": [dict(row) for row in rows],
        }

    def get_release_alert_counts(
        self,
        today: str,
        soon_through: str,
    ) -> dict[str, int]:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    SUM(CASE WHEN release_date < ? THEN 1 ELSE 0 END)
                        AS released,
                    SUM(CASE WHEN release_date = ? THEN 1 ELSE 0 END)
                        AS today,
                    SUM(
                        CASE
                            WHEN release_date > ? AND release_date <= ?
                                THEN 1
                            ELSE 0
                        END
                    ) AS soon
                FROM looking_out_for
                """,
                (today, today, today, soon_through),
            ).fetchone()
        return {
            "released": int(row["released"] or 0),
            "today": int(row["today"] or 0),
            "soon": int(row["soon"] or 0),
        }

    def get_release_alerts_enabled(self) -> bool:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT setting_value
                FROM app_settings
                WHERE setting_key = 'release_alerts_enabled'
                """
            ).fetchone()
        return row is None or str(row["setting_value"]).casefold() == "true"

    def set_release_alerts_enabled(self, enabled: bool) -> bool:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO app_settings (setting_key, setting_value)
                VALUES ('release_alerts_enabled', ?)
                ON CONFLICT(setting_key) DO UPDATE SET
                    setting_value = excluded.setting_value,
                    updated_at = CURRENT_TIMESTAMP
                """,
                ("true" if enabled else "false",),
            )
        return enabled
