import unittest

from app.advanced_filters import AdvancedMovieFilters
from app.tmdb_client import BASE_URL, TMDBClient


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return self.payload


class FakeSession:
    def __init__(self) -> None:
        self.last_request: dict | None = None
        self.call_count: int = 0

    def get(self, url: str, **kwargs) -> FakeResponse:
        self.call_count += 1
        self.last_request = {
            "url": url,
            **kwargs,
        }

        if url.endswith("/discover/movie"):
            return FakeResponse(
                {
                    "page": 2,
                    "results": [
                        {"id": 603, "title": "The Matrix"}
                    ],
                    "total_pages": 10,
                    "total_results": 200,
                }
            )

        if url.endswith("/search/person"):
            return FakeResponse(
                {
                    "page": 1,
                    "results": [
                        {
                            "id": 525,
                            "name": "Christopher Nolan",
                        }
                    ],
                    "total_pages": 1,
                    "total_results": 1,
                }
            )

        if url.endswith("/search/company"):
            return FakeResponse(
                {
                    "page": 1,
                    "results": [
                        {
                            "id": 9993,
                            "name": "Syncopy",
                        }
                    ],
                    "total_pages": 1,
                    "total_results": 1,
                }
            )

        if url.endswith("/person/525/movie_credits"):
            return FakeResponse(
                {
                    "id": 525,
                    "crew": [
                        {
                            "id": 27205,
                            "title": "Inception",
                            "job": "Director",
                        }
                    ],
                }
            )

        return FakeResponse(
            {
                "id": 603,
                "origin_country": ["US"],
                "production_countries": [
                    {
                        "iso_3166_1": "US",
                        "name": "United States of America",
                    }
                ],
            }
        )


class TMDBClientAdvancedDiscoveryTests(unittest.TestCase):
    def test_discover_movies_sends_filter_params(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()
        filters = AdvancedMovieFilters(
            include_genre_ids=[878],
            exclude_origin_countries=["IN", "PK"],
            minimum_rating=7,
            minimum_vote_count=100,
        )

        result = client.discover_movies(filters, page=2)

        request = client.session.last_request
        self.assertEqual(
            request["url"],
            f"{BASE_URL}/discover/movie",
        )
        self.assertEqual(request["params"]["with_genres"], "878")
        self.assertEqual(request["params"]["vote_average.gte"], 7)
        self.assertEqual(request["params"]["vote_count.gte"], 100)
        self.assertEqual(request["params"]["page"], 2)
        self.assertNotIn(
            "exclude_origin_countries",
            request["params"],
        )
        self.assertEqual(result["total_pages"], 10)

    def test_discover_movies_rejects_invalid_page(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()

        with self.assertRaises(ValueError):
            client.discover_movies(AdvancedMovieFilters(), page=0)

    def test_filter_details_do_not_append_keywords(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()

        result = client.get_movie_filter_details(603)

        request = client.session.last_request
        self.assertEqual(
            request["url"],
            f"{BASE_URL}/movie/603",
        )
        self.assertNotIn("params", request)
        self.assertEqual(result["origin_country"], ["US"])

    def test_people_search_is_ready_for_autocomplete(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()

        result = client.search_people("  Nolan  ")

        request = client.session.last_request
        self.assertEqual(
            request["url"],
            f"{BASE_URL}/search/person",
        )
        self.assertEqual(request["params"]["query"], "Nolan")
        self.assertFalse(request["params"]["include_adult"])
        self.assertEqual(
            result["results"][0]["name"],
            "Christopher Nolan",
        )

    def test_company_search_is_ready_for_autocomplete(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()

        result = client.search_companies("Syncopy")

        request = client.session.last_request
        self.assertEqual(
            request["url"],
            f"{BASE_URL}/search/company",
        )
        self.assertEqual(request["params"]["query"], "Syncopy")
        self.assertEqual(result["results"][0]["id"], 9993)

    def test_person_movie_credits_are_available(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()

        result = client.get_person_movie_credits(525)

        request = client.session.last_request
        self.assertEqual(
            request["url"],
            f"{BASE_URL}/person/525/movie_credits",
        )
        self.assertEqual(result["crew"][0]["job"], "Director")

    def test_lookup_inputs_are_validated(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()

        invalid_calls = [
            lambda: client.search_people("   "),
            lambda: client.search_companies("Syncopy", page=0),
            lambda: client.get_person_movie_credits(0),
        ]

        for call in invalid_calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError):
                    call()

    def test_discover_movies_caches_in_sqlite_and_respects_force_refresh(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()

        filters = AdvancedMovieFilters(include_genre_ids=[28, 12])

        # 1. First call fetches via session (call_count=1)
        res1 = client.discover_movies(filters, page=1)
        self.assertEqual(client.session.call_count, 1)
        self.assertEqual(res1["results"][0]["id"], 603)

        # 2. Second call with same filters and page hits SQLite cache (call_count stays 1!)
        res2 = client.discover_movies(filters, page=1)
        self.assertEqual(client.session.call_count, 1)
        self.assertEqual(res2["results"][0]["title"], "The Matrix")

        # 3. Third call with force_refresh=True forces network call (call_count=2)
        res3 = client.discover_movies(filters, page=1, force_refresh=True)
        self.assertEqual(client.session.call_count, 2)
        self.assertEqual(res3["results"][0]["id"], 603)

    def test_person_movie_credits_caches_in_sqlite_and_respects_force_refresh(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()

        # 1. First call fetches via session
        res1 = client.get_person_movie_credits(525)
        self.assertEqual(client.session.call_count, 1)
        self.assertEqual(res1["crew"][0]["title"], "Inception")

        # 2. Second call uses SQLite cache (call_count stays 1!)
        res2 = client.get_person_movie_credits(525)
        self.assertEqual(client.session.call_count, 1)
        self.assertEqual(res2["crew"][0]["id"], 27205)

        # 3. Third call with force_refresh=True forces network call (call_count=2)
        res3 = client.get_person_movie_credits(525, force_refresh=True)
        self.assertEqual(client.session.call_count, 2)


if __name__ == "__main__":
    unittest.main()
