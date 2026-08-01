import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class FakeAdvancedSearchService:
    def __init__(self) -> None:
        self.last_search: dict | None = None

    def search(
        self,
        preference_id: int | None = None,
        page: int = 1,
        filters: dict | None = None,
    ) -> dict:
        if page < 1:
            raise ValueError("Advanced Search page must be at least 1.")
        if preference_id == 999:
            raise LookupError("Search preference was not found.")

        self.last_search = {
            "preference_id": preference_id,
            "page": page,
            "filters": filters,
        }
        return {
            "preference": {
                "preference_id": preference_id or 1,
                "name": "American Sci-Fi",
                "is_default": preference_id is None,
            },
            "page": page,
            "result_count": 1,
            "results": [{"id": 603, "title": "The Matrix"}],
        }


class AdvancedSearchEndpointTests(unittest.TestCase):
    def test_advanced_search_route_is_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn(
            "/movies/discover/advanced",
            route_paths,
        )

    def test_advanced_search_uses_selected_preference(self) -> None:
        service = FakeAdvancedSearchService()

        with patch.object(
            main,
            "advanced_search_service",
            service,
        ):
            result = main.advanced_search(
                preference_id=5,
                page=2,
            )

        self.assertEqual(
            service.last_search,
            {"preference_id": 5, "page": 2, "filters": None},
        )
        self.assertEqual(result["page"], 2)

    def test_advanced_search_can_use_default_preference(self) -> None:
        service = FakeAdvancedSearchService()

        with patch.object(
            main,
            "advanced_search_service",
            service,
        ):
            result = main.advanced_search()

        self.assertTrue(result["preference"]["is_default"])

    def test_missing_preference_returns_404(self) -> None:
        service = FakeAdvancedSearchService()

        with patch.object(
            main,
            "advanced_search_service",
            service,
        ):
            with self.assertRaises(HTTPException) as context:
                main.advanced_search(preference_id=999)

        self.assertEqual(context.exception.status_code, 404)

    def test_direct_filters_can_run_without_saving_a_profile(self) -> None:
        service = FakeAdvancedSearchService()
        request = main.AdvancedSearchExecutionRequest(
            filters=main.AdvancedFiltersRequest(
                include_genre_ids=[878],
                exclude_origin_countries=["IN", "PK"],
            )
        )

        with patch.object(main, "advanced_search_service", service):
            main.advanced_search_with_filters(request)

        self.assertEqual(
            service.last_search["filters"]["include_genre_ids"],
            [878],
        )

    def test_invalid_page_returns_400(self) -> None:
        service = FakeAdvancedSearchService()

        with patch.object(
            main,
            "advanced_search_service",
            service,
        ):
            with self.assertRaises(HTTPException) as context:
                main.advanced_search(page=0)

        self.assertEqual(context.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
