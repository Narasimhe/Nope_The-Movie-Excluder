import json
from typing import Any

from app.advanced_filters import AdvancedMovieFilters
from app.database import get_connection
from app.search_preference_repository import SearchPreferenceRepository


class SearchStateRepository:
    """Stores the single active discovery workspace for this local app."""

    def get_state(self) -> dict[str, Any]:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM search_state
                WHERE state_id = 1
                """
            ).fetchone()

        if row is None:
            return self.save_state(
                mode="simple",
                filters={},
                personal_filters=None,
                selected_preference_id=None,
                filters_collapsed=False,
            )

        return self._row_to_state(row)

    def save_state(
        self,
        *,
        mode: str,
        filters: AdvancedMovieFilters | dict[str, Any],
        personal_filters: dict[str, Any] | None,
        selected_preference_id: int | None,
        filters_collapsed: bool,
    ) -> dict[str, Any]:
        if mode not in {"simple", "advanced", "super"}:
            raise ValueError("Search mode must be simple, advanced, or super.")
        if not isinstance(filters_collapsed, bool):
            raise ValueError("filters_collapsed must be true or false.")

        filters_json = SearchPreferenceRepository._serialize_filters(filters)
        personal_filters_json = (
            SearchPreferenceRepository._serialize_personal_filters(
                personal_filters
            )
        )

        if selected_preference_id is not None:
            SearchPreferenceRepository._validate_preference_id(
                selected_preference_id
            )
            with get_connection() as connection:
                exists = connection.execute(
                    """
                    SELECT 1
                    FROM search_preferences
                    WHERE preference_id = ?
                    """,
                    (selected_preference_id,),
                ).fetchone()
            if exists is None:
                raise ValueError("Selected search preference was not found.")

        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO search_state (
                    state_id,
                    mode,
                    filters_json,
                    personal_filters_json,
                    selected_preference_id,
                    filters_collapsed,
                    updated_at
                )
                VALUES (1, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(state_id) DO UPDATE SET
                    mode = excluded.mode,
                    filters_json = excluded.filters_json,
                    personal_filters_json = excluded.personal_filters_json,
                    selected_preference_id = excluded.selected_preference_id,
                    filters_collapsed = excluded.filters_collapsed,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    mode,
                    filters_json,
                    personal_filters_json,
                    selected_preference_id,
                    int(filters_collapsed),
                ),
            )

        return self.get_state()

    @staticmethod
    def _row_to_state(row) -> dict[str, Any]:
        return {
            "mode": row["mode"],
            "filters": json.loads(row["filters_json"]),
            "personal_filters": json.loads(
                row["personal_filters_json"]
            ),
            "selected_preference_id": row["selected_preference_id"],
            "filters_collapsed": bool(row["filters_collapsed"]),
            "updated_at": row["updated_at"],
        }
