import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class FakeSearchPreferenceRepository:
    def __init__(self) -> None:
        self.preferences = {
            1: {
                "preference_id": 1,
                "name": "American Sci-Fi",
                "filters": {
                    "include_genre_ids": [878],
                    "include_origin_countries": ["US"],
                },
                "is_default": False,
            }
        }
        self.created: dict | None = None
        self.updated: dict | None = None
        self.default_id: int | None = None

    def create_preference(
        self,
        name: str,
        filters: dict,
        *,
        is_default: bool = False,
    ) -> dict:
        if not name.strip():
            raise ValueError(
                "Search preference name cannot be empty."
            )

        self.created = {
            "name": name,
            "filters": filters,
            "is_default": is_default,
        }
        return {
            "preference_id": 2,
            **self.created,
        }

    def list_preferences(self) -> list[dict]:
        return list(self.preferences.values())

    def get_preference(self, preference_id: int) -> dict | None:
        return self.preferences.get(preference_id)

    def update_preference(
        self,
        preference_id: int,
        name: str,
        filters: dict,
    ) -> dict:
        self.updated = {
            "preference_id": preference_id,
            "name": name,
            "filters": filters,
            "is_default": False,
        }
        return self.updated

    def set_default(self, preference_id: int) -> dict:
        self.default_id = preference_id
        preference = dict(self.preferences[preference_id])
        preference["is_default"] = True
        return preference

    def delete_preference(self, preference_id: int) -> bool:
        return self.preferences.pop(preference_id, None) is not None


class SearchPreferenceEndpointTests(unittest.TestCase):
    def test_search_preference_routes_are_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/search-preferences", route_paths)
        self.assertIn(
            "/search-preferences/{preference_id}",
            route_paths,
        )
        self.assertIn(
            "/search-preferences/{preference_id}/default",
            route_paths,
        )

    def test_preference_can_be_created(self) -> None:
        repository = FakeSearchPreferenceRepository()
        request = main.SearchPreferenceCreateRequest(
            name="American Sci-Fi",
            filters=main.AdvancedFiltersRequest(
                include_genre_ids=[878],
                include_origin_countries=["US"],
                exclude_origin_countries=["IN", "PK"],
                minimum_rating=7,
            ),
            is_default=True,
        )

        with patch.object(
            main,
            "search_preference_repository",
            repository,
        ):
            result = main.create_search_preference(request)

        self.assertTrue(repository.created["is_default"])
        self.assertEqual(
            repository.created["filters"][
                "exclude_origin_countries"
            ],
            ["IN", "PK"],
        )
        self.assertEqual(
            result["preference"]["name"],
            "American Sci-Fi",
        )

    def test_invalid_preference_returns_400(self) -> None:
        repository = FakeSearchPreferenceRepository()
        request = main.SearchPreferenceCreateRequest(
            name="   ",
            filters=main.AdvancedFiltersRequest(),
        )

        with patch.object(
            main,
            "search_preference_repository",
            repository,
        ):
            with self.assertRaises(HTTPException) as context:
                main.create_search_preference(request)

        self.assertEqual(context.exception.status_code, 400)

    def test_preferences_can_be_listed_and_read(self) -> None:
        repository = FakeSearchPreferenceRepository()

        with patch.object(
            main,
            "search_preference_repository",
            repository,
        ):
            listed = main.list_search_preferences()
            selected = main.get_search_preference(1)

        self.assertEqual(len(listed), 1)
        self.assertEqual(selected["preference_id"], 1)

    def test_missing_preference_returns_404(self) -> None:
        repository = FakeSearchPreferenceRepository()

        with patch.object(
            main,
            "search_preference_repository",
            repository,
        ):
            with self.assertRaises(HTTPException) as context:
                main.get_search_preference(999)

        self.assertEqual(context.exception.status_code, 404)

    def test_preference_can_be_updated(self) -> None:
        repository = FakeSearchPreferenceRepository()
        request = main.SearchPreferenceUpdateRequest(
            name="American Thrillers",
            filters=main.AdvancedFiltersRequest(
                include_genre_ids=[53],
                include_origin_countries=["US"],
            ),
        )

        with patch.object(
            main,
            "search_preference_repository",
            repository,
        ):
            result = main.update_search_preference(1, request)

        self.assertEqual(
            repository.updated["filters"]["include_genre_ids"],
            [53],
        )
        self.assertEqual(
            result["preference"]["name"],
            "American Thrillers",
        )

    def test_preference_can_be_set_as_default(self) -> None:
        repository = FakeSearchPreferenceRepository()

        with patch.object(
            main,
            "search_preference_repository",
            repository,
        ):
            result = main.set_default_search_preference(1)

        self.assertEqual(repository.default_id, 1)
        self.assertTrue(result["preference"]["is_default"])

    def test_preference_can_be_deleted(self) -> None:
        repository = FakeSearchPreferenceRepository()

        with patch.object(
            main,
            "search_preference_repository",
            repository,
        ):
            result = main.delete_search_preference(1)

        self.assertEqual(
            result["message"],
            "Search preference deleted",
        )

    def test_deleting_missing_preference_returns_404(self) -> None:
        repository = FakeSearchPreferenceRepository()

        with patch.object(
            main,
            "search_preference_repository",
            repository,
        ):
            with self.assertRaises(HTTPException) as context:
                main.delete_search_preference(999)

        self.assertEqual(context.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
