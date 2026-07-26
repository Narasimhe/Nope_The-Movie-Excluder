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

    def get(self, url: str, **kwargs) -> FakeResponse:
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


if __name__ == "__main__":
    unittest.main()
