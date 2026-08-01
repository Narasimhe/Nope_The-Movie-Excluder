import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class FakeMovieService:
    def __init__(self) -> None:
        self.requested_status: str | None = None

    def get_movies_by_status_page(self, status: str, page: int) -> dict:
        allowed = {
            "new_discovery",
            "watch_later",
            "watched",
            "rewatch",
            "excluded",
        }

        if status not in allowed:
            raise ValueError(f"Invalid movie status: {status!r}.")

        self.requested_status = status
        return {
            "page": page,
            "total_results": 1,
            "total_pages": 1,
            "results": [{
                "tmdb_id": 603,
                "title": "The Matrix",
                "genres": [
                    {"tmdb_genre_id": 878, "name": "Science Fiction"}
                ],
                "user_data": {
                    "tmdb_id": 603,
                    "status": status,
                },
            }],
        }


class MovieStatusListEndpointTests(unittest.TestCase):
    def test_status_list_route_is_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/movies/status/{status}", route_paths)

    def test_status_list_returns_exact_status_results(self) -> None:
        fake_service = FakeMovieService()

        with patch.object(main, "movie_service", fake_service):
            result = main.get_movies_by_status("watch_later")

        self.assertEqual(
            fake_service.requested_status,
            "watch_later",
        )
        self.assertEqual(
            result["results"][0]["user_data"]["status"],
            "watch_later",
        )
        self.assertEqual(
            result["results"][0]["genres"][0]["name"],
            "Science Fiction",
        )

    def test_invalid_status_returns_400(self) -> None:
        fake_service = FakeMovieService()

        with patch.object(main, "movie_service", fake_service):
            with self.assertRaises(HTTPException) as context:
                main.get_movies_by_status("maybe")

        self.assertEqual(context.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
