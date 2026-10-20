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


    def get_person(self, person_id: int) -> dict:
        return {
            "id": person_id,
            "name": "Christopher Nolan",
            "known_for_department": "Directing",
            "profile_path": "/nolan.jpg",
        }

    def get_person_movie_credits(self, person_id: int) -> dict:
        return {
            "id": person_id,
            "cast": [
                {
                    "id": 804706,
                    "title": "Tarantella",
                    "character": "Man in Black",
                    "release_date": "1990-09-12",
                    "poster_path": "/tarantella.jpg",
                }
            ],
            "crew": [
                {
                    "id": 872585,
                    "title": "Oppenheimer",
                    "job": "Director",
                    "department": "Directing",
                    "release_date": "2023-07-19",
                    "poster_path": "/oppenheimer.jpg",
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
        self.assertIn("/people/{person_id}/filmography", route_paths)

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

    def test_person_filmography_returns_directing_and_acting_credits(self) -> None:
        client = FakeTMDBLookupClient()

        with patch.object(main, "tmdb_lookup_client", client):
            result = main.get_person_filmography(525)

        self.assertEqual(result["person"]["id"], 525)
        self.assertEqual(result["person"]["name"], "Christopher Nolan")
        self.assertEqual(result["directing_count"], 1)
        self.assertEqual(result["acting_count"], 1)
        self.assertEqual(result["total_count"], 2)

    def test_person_filmography_department_filtering(self) -> None:
        client = FakeTMDBLookupClient()

        with patch.object(main, "tmdb_lookup_client", client):
            directing_result = main.get_person_filmography(525, department="directing")
            acting_result = main.get_person_filmography(525, department="acting")

        self.assertEqual(len(directing_result["movies"]), 1)
        self.assertEqual(directing_result["movies"][0]["title"], "Oppenheimer")
        self.assertEqual(len(acting_result["movies"]), 1)
        self.assertEqual(acting_result["movies"][0]["title"], "Tarantella")


if __name__ == "__main__":
    unittest.main()
