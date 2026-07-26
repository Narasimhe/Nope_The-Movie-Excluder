import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class FakeTMDBLookupClient:
    def __init__(self) -> None:
        self.last_call: dict | None = None

    def search_people(self, query: str, page: int = 1) -> dict:
        if not query.strip():
            raise ValueError("TMDB search query cannot be empty.")

        self.last_call = {
            "kind": "people",
            "query": query,
            "page": page,
        }
        return {
            "page": page,
            "total_pages": 1,
            "total_results": 1,
            "results": [
                {
                    "id": 525,
                    "name": "Christopher Nolan",
                    "known_for_department": "Directing",
                    "profile_path": "/nolan.jpg",
                    "known_for": [
                        {"title": "Inception"},
                        {"title": "Interstellar"},
                    ],
                }
            ],
        }

    def search_companies(self, query: str, page: int = 1) -> dict:
        self.last_call = {
            "kind": "companies",
            "query": query,
            "page": page,
        }
        return {
            "page": page,
            "total_pages": 1,
            "total_results": 1,
            "results": [
                {
                    "id": 9993,
                    "name": "Syncopy",
                    "origin_country": "GB",
                    "logo_path": "/syncopy.png",
                }
            ],
        }


class PeopleCompanyLookupEndpointTests(unittest.TestCase):
    def test_lookup_routes_are_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/people/search", route_paths)
        self.assertIn("/companies/search", route_paths)

    def test_people_results_are_shaped_for_autocomplete(self) -> None:
        client = FakeTMDBLookupClient()

        with patch.object(main, "tmdb_lookup_client", client):
            result = main.search_people("Nolan", page=1)

        self.assertEqual(result["results"][0]["id"], 525)
        self.assertEqual(
            result["results"][0]["known_for_titles"],
            ["Inception", "Interstellar"],
        )
        self.assertEqual(client.last_call["kind"], "people")

    def test_company_results_are_shaped_for_autocomplete(self) -> None:
        client = FakeTMDBLookupClient()

        with patch.object(main, "tmdb_lookup_client", client):
            result = main.search_companies("Syncopy", page=1)

        self.assertEqual(result["results"][0]["id"], 9993)
        self.assertEqual(
            result["results"][0]["origin_country"],
            "GB",
        )
        self.assertEqual(client.last_call["kind"], "companies")

    def test_empty_people_query_returns_400(self) -> None:
        client = FakeTMDBLookupClient()

        with patch.object(main, "tmdb_lookup_client", client):
            with self.assertRaises(HTTPException) as context:
                main.search_people("   ")

        self.assertEqual(context.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
