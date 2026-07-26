import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main
from app.movie_status import MovieStatus


class FakeSuperAdvancedSearchService:
    def __init__(self) -> None:
        self.last_search: dict | None = None

    def search(
        self,
        preference_id: int | None = None,
        page: int = 1,
        included_statuses=None,
        include_untracked: bool = True,
        notes_query: str | None = None,
        favorite_only: bool = False,
    ) -> dict:
        if preference_id == 999:
            raise LookupError("Search preference was not found.")
        if "maybe" in (included_statuses or []):
            raise ValueError("Invalid movie status.")
        if notes_query is not None and not notes_query.strip():
            raise ValueError("notes_query cannot be empty.")

        self.last_search = {
            "preference_id": preference_id,
            "page": page,
            "included_statuses": included_statuses,
            "include_untracked": include_untracked,
            "notes_query": notes_query,
            "favorite_only": favorite_only,
        }
        return {
            "page": page,
            "status_filter": {
                "included_statuses": included_statuses,
                "include_untracked": include_untracked,
            },
            "notes_filter": {
                "query": notes_query,
            },
            "favorite_filter": {
                "favorite_only": favorite_only,
            },
            "results": [],
        }


class SuperAdvancedSearchEndpointTests(unittest.TestCase):
    def test_super_advanced_route_is_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn(
            "/movies/discover/super-advanced",
            route_paths,
        )

    def test_default_status_options_are_forwarded(self) -> None:
        service = FakeSuperAdvancedSearchService()
        request = main.SuperAdvancedSearchRequest()

        with patch.object(
            main,
            "super_advanced_search_service",
            service,
        ):
            main.super_advanced_search(request)

        self.assertEqual(
            service.last_search["included_statuses"],
            [
                MovieStatus.NEW_DISCOVERY,
                MovieStatus.WATCH_LATER,
            ],
        )
        self.assertTrue(
            service.last_search["include_untracked"]
        )

    def test_custom_status_options_are_forwarded(self) -> None:
        service = FakeSuperAdvancedSearchService()
        request = main.SuperAdvancedSearchRequest(
            preference_id=3,
            page=2,
            included_statuses=[
                MovieStatus.WATCHED,
                MovieStatus.REWATCH,
            ],
            include_untracked=False,
            notes_query="cold ambience",
            favorite_only=True,
        )

        with patch.object(
            main,
            "super_advanced_search_service",
            service,
        ):
            result = main.super_advanced_search(request)

        self.assertEqual(
            service.last_search["preference_id"],
            3,
        )
        self.assertEqual(service.last_search["page"], 2)
        self.assertFalse(
            result["status_filter"]["include_untracked"]
        )
        self.assertEqual(
            service.last_search["notes_query"],
            "cold ambience",
        )
        self.assertTrue(
            service.last_search["favorite_only"]
        )

    def test_missing_preference_returns_404(self) -> None:
        service = FakeSuperAdvancedSearchService()
        request = main.SuperAdvancedSearchRequest(
            preference_id=999,
        )

        with patch.object(
            main,
            "super_advanced_search_service",
            service,
        ):
            with self.assertRaises(HTTPException) as context:
                main.super_advanced_search(request)

        self.assertEqual(context.exception.status_code, 404)

    def test_invalid_status_returns_400(self) -> None:
        service = FakeSuperAdvancedSearchService()
        request = main.SuperAdvancedSearchRequest()
        request.included_statuses = ["maybe"]

        with patch.object(
            main,
            "super_advanced_search_service",
            service,
        ):
            with self.assertRaises(HTTPException) as context:
                main.super_advanced_search(request)

        self.assertEqual(context.exception.status_code, 400)

    def test_blank_notes_query_returns_400(self) -> None:
        service = FakeSuperAdvancedSearchService()
        request = main.SuperAdvancedSearchRequest(
            notes_query="   ",
        )

        with patch.object(
            main,
            "super_advanced_search_service",
            service,
        ):
            with self.assertRaises(HTTPException) as context:
                main.super_advanced_search(request)

        self.assertEqual(context.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
