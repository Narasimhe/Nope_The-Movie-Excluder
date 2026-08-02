import unittest
from unittest.mock import patch

from app import main


class FakeMovieService:
    def __init__(self) -> None:
        self.requested_id: int | None = None

    def get_movie(self, tmdb_id: int) -> dict:
        self.requested_id = tmdb_id
        return {
            "tmdb_id": tmdb_id,
            "title": "The Matrix",
            "genres": [
                {
                    "tmdb_genre_id": 878,
                    "name": "Science Fiction",
                }
            ],
            "keywords": [
                {
                    "keyword_id": 1,
                    "tmdb_keyword_id": 123,
                    "name": "artificial reality",
                    "is_custom": False,
                    "position": 1,
                }
            ],
        }

    def get_related_movies(self, tmdb_id: int, limit: int = 6) -> dict:
        self.requested_id = tmdb_id
        return {
            "tmdb_id": tmdb_id,
            "result_count": 1,
            "results": [{"tmdb_id": 604, "title": "Related"}][:limit],
        }


class MovieDetailsEndpointTests(unittest.TestCase):
    def test_movie_details_route_is_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/movies/{tmdb_id}", route_paths)
        self.assertIn("/movies/{tmdb_id}/related", route_paths)

    def test_movie_details_calls_movie_service(self) -> None:
        fake_service = FakeMovieService()

        with patch.object(main, "movie_service", fake_service):
            result = main.get_movie_details(603)

        self.assertEqual(fake_service.requested_id, 603)
        self.assertEqual(result["tmdb_id"], 603)
        self.assertEqual(result["genres"][0]["name"], "Science Fiction")
        self.assertEqual(
            result["keywords"][0]["name"],
            "artificial reality",
        )

    def test_related_movies_calls_movie_service(self) -> None:
        fake_service = FakeMovieService()
        with patch.object(main, "movie_service", fake_service):
            result = main.get_related_movies(603, limit=4)

        self.assertEqual(fake_service.requested_id, 603)
        self.assertEqual(result["results"][0]["tmdb_id"], 604)


if __name__ == "__main__":
    unittest.main()
