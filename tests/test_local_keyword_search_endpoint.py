import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class FakeMovieService:
    def __init__(self) -> None:
        self.request: tuple[str, str] | None = None

    def search_local_movies_by_keyword_page(
        self,
        query: str,
        keyword_type: str,
        page: int,
    ) -> dict:
        if not query.strip():
            raise ValueError("Keyword search name cannot be empty.")

        self.request = (query, keyword_type)
        return {
            "query": query,
            "keyword_type": keyword_type,
            "page": page,
            "total_results": 1,
            "total_pages": 1,
            "movies": [
                {
                    "tmdb_id": 1726,
                    "title": "Iron Man",
                    "genres": [],
                    "user_data": {
                        "status": "watched",
                    },
                    "matched_keywords": [
                        {
                            "keyword_id": 51,
                            "name": "Marvel",
                            "is_custom": True,
                        }
                    ],
                }
            ],
        }


class LocalKeywordSearchEndpointTests(unittest.TestCase):
    def test_local_keyword_search_route_is_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/movies/keywords/search", route_paths)

    def test_local_keyword_search_returns_cached_movies(self) -> None:
        fake_service = FakeMovieService()

        with patch.object(main, "movie_service", fake_service):
            result = main.search_local_movies_by_keyword(
                "marvel",
                main.KeywordType.CUSTOM,
            )

        self.assertEqual(
            fake_service.request,
            ("marvel", "custom"),
        )
        self.assertEqual(result["total_results"], 1)
        self.assertEqual(
            result["movies"][0]["user_data"]["status"],
            "watched",
        )

    def test_blank_local_keyword_query_returns_400(self) -> None:
        fake_service = FakeMovieService()

        with patch.object(main, "movie_service", fake_service):
            with self.assertRaises(HTTPException) as context:
                main.search_local_movies_by_keyword(
                    "   ",
                    main.KeywordType.ALL,
                )

        self.assertEqual(context.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
