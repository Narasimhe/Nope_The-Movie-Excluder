import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class FakeMovieService:
    def __init__(self) -> None:
        self.updated: tuple[int, str] | None = None

    def set_movie_status(
        self,
        tmdb_id: int,
        status: str,
    ) -> dict:
        allowed = {
            "new_discovery",
            "watch_later",
            "watched",
            "rewatch",
            "excluded",
        }

        if status not in allowed:
            raise ValueError(f"Invalid movie status: {status!r}.")

        self.updated = (tmdb_id, status)
        return {
            "tmdb_id": tmdb_id,
            "status": status,
            "verdict": None,
            "notes": None,
        }


class MovieStatusEndpointTests(unittest.TestCase):
    def test_status_route_is_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/movies/{tmdb_id}/status", route_paths)

    def test_status_can_be_updated(self) -> None:
        fake_service = FakeMovieService()
        request = main.MovieStatusRequest(status="watch_later")

        with patch.object(main, "movie_service", fake_service):
            result = main.set_movie_status(603, request)

        self.assertEqual(
            fake_service.updated,
            (603, "watch_later"),
        )
        self.assertEqual(
            result["user_movie_data"]["status"],
            "watch_later",
        )

    def test_invalid_status_returns_400(self) -> None:
        fake_service = FakeMovieService()
        request = main.MovieStatusRequest(status="maybe")

        with patch.object(main, "movie_service", fake_service):
            with self.assertRaises(HTTPException) as context:
                main.set_movie_status(603, request)

        self.assertEqual(context.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
