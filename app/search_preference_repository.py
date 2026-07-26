import json
import sqlite3
from typing import Any

from app.advanced_filters import AdvancedMovieFilters
from app.database import get_connection


class SearchPreferenceRepository:
    def create_preference(
        self,
        name: str,
        filters: AdvancedMovieFilters | dict[str, Any],
        *,
        is_default: bool = False,
    ) -> dict:
        cleaned_name = self._clean_name(name)
        filters_json = self._serialize_filters(filters)

        try:
            with get_connection() as connection:
                if is_default:
                    self._clear_default(connection)

                cursor = connection.execute(
                    """
                    INSERT INTO search_preferences (
                        name,
                        filters_json,
                        is_default
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        cleaned_name,
                        filters_json,
                        int(is_default),
                    ),
                )
                preference_id = cursor.lastrowid
        except sqlite3.IntegrityError as error:
            raise ValueError(
                f"A search preference named {cleaned_name!r} "
                "already exists."
            ) from error

        preference = self.get_preference(preference_id)

        if preference is None:
            raise RuntimeError(
                "Search preference was saved but could not be read."
            )

        return preference

    def update_preference(
        self,
        preference_id: int,
        name: str,
        filters: AdvancedMovieFilters | dict[str, Any],
    ) -> dict:
        self._validate_preference_id(preference_id)
        cleaned_name = self._clean_name(name)
        filters_json = self._serialize_filters(filters)

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    """
                    UPDATE search_preferences
                    SET
                        name = ?,
                        filters_json = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE preference_id = ?
                    """,
                    (
                        cleaned_name,
                        filters_json,
                        preference_id,
                    ),
                )
        except sqlite3.IntegrityError as error:
            raise ValueError(
                f"A search preference named {cleaned_name!r} "
                "already exists."
            ) from error

        if cursor.rowcount == 0:
            raise ValueError("Search preference was not found.")

        preference = self.get_preference(preference_id)

        if preference is None:
            raise RuntimeError(
                "Search preference was updated but could not be read."
            )

        return preference

    def get_preference(self, preference_id: int) -> dict | None:
        self._validate_preference_id(preference_id)

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM search_preferences
                WHERE preference_id = ?
                """,
                (preference_id,),
            ).fetchone()

        return self._row_to_preference(row)

    def get_preference_by_name(self, name: str) -> dict | None:
        cleaned_name = self._clean_name(name)

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM search_preferences
                WHERE name = ? COLLATE NOCASE
                """,
                (cleaned_name,),
            ).fetchone()

        return self._row_to_preference(row)

    def get_default_preference(self) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM search_preferences
                WHERE is_default = 1
                """
            ).fetchone()

        return self._row_to_preference(row)

    def list_preferences(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM search_preferences
                ORDER BY name COLLATE NOCASE
                """
            ).fetchall()

        return [
            self._row_to_preference(row)
            for row in rows
        ]

    def set_default(self, preference_id: int) -> dict:
        self._validate_preference_id(preference_id)

        with get_connection() as connection:
            exists = connection.execute(
                """
                SELECT 1
                FROM search_preferences
                WHERE preference_id = ?
                """,
                (preference_id,),
            ).fetchone()

            if exists is None:
                raise ValueError("Search preference was not found.")

            self._clear_default(connection)
            connection.execute(
                """
                UPDATE search_preferences
                SET
                    is_default = 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE preference_id = ?
                """,
                (preference_id,),
            )

        preference = self.get_preference(preference_id)

        if preference is None:
            raise RuntimeError(
                "Default search preference could not be read."
            )

        return preference

    def delete_preference(self, preference_id: int) -> bool:
        self._validate_preference_id(preference_id)

        with get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM search_preferences
                WHERE preference_id = ?
                """,
                (preference_id,),
            )

        return cursor.rowcount > 0

    @staticmethod
    def _clear_default(connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            UPDATE search_preferences
            SET
                is_default = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE is_default = 1
            """
        )

    @staticmethod
    def _validate_preference_id(preference_id: int) -> None:
        if (
            isinstance(preference_id, bool)
            or not isinstance(preference_id, int)
            or preference_id <= 0
        ):
            raise ValueError(
                "Search preference ID must be a positive integer."
            )

    @staticmethod
    def _clean_name(name: str) -> str:
        if not isinstance(name, str):
            raise ValueError("Search preference name must be text.")

        cleaned_name = " ".join(name.split())

        if not cleaned_name:
            raise ValueError("Search preference name cannot be empty.")

        if len(cleaned_name) > 100:
            raise ValueError(
                "Search preference name cannot exceed 100 characters."
            )

        return cleaned_name

    @staticmethod
    def _serialize_filters(
        filters: AdvancedMovieFilters | dict[str, Any],
    ) -> str:
        if isinstance(filters, AdvancedMovieFilters):
            validated_filters = filters
        elif isinstance(filters, dict):
            validated_filters = AdvancedMovieFilters(**filters)
        else:
            raise ValueError(
                "Search filters must be an AdvancedMovieFilters "
                "instance or dictionary."
            )

        return json.dumps(
            validated_filters.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
        )

    @staticmethod
    def _row_to_preference(
        row: sqlite3.Row | None,
    ) -> dict | None:
        if row is None:
            return None

        try:
            stored_filters = json.loads(row["filters_json"])
            filters = AdvancedMovieFilters(
                **stored_filters
            ).to_dict()
        except (json.JSONDecodeError, TypeError, ValueError) as error:
            raise RuntimeError(
                "Stored search preference contains invalid filters."
            ) from error

        return {
            "preference_id": row["preference_id"],
            "name": row["name"],
            "filters": filters,
            "is_default": bool(row["is_default"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
