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

    def test_library_search_route_is_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/movies/library/search", route_paths)

    def test_library_search_endpoint(self) -> None:
        with patch.object(main.movie_service, "search_user_library") as mock_search:
            mock_search.return_value = [{"tmdb_id": 603, "title": "The Matrix"}]
            result = main.search_personal_library(query="matrix", status="watched")
            mock_search.assert_called_once_with("matrix", "watched")
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["title"], "The Matrix")

    def test_library_keywords_endpoint(self) -> None:
        route_paths = {route.path for route in main.app.routes}
        self.assertIn("/movies/library/keywords", route_paths)

        with patch.object(main.movie_service, "search_library_keywords") as mock_search:
            mock_search.return_value = [{"id": 1, "name": "cyberpunk"}]
            result = main.search_library_keywords(query="cyber")
            mock_search.assert_called_once_with(query="cyber")
            self.assertEqual(result["results"], [{"id": 1, "name": "cyberpunk"}])

    def test_get_general_entry_endpoint(self) -> None:
        route_paths = {route.path for route in main.app.routes}
        self.assertIn("/entries/{entry_id}", route_paths)

        with patch.object(main.general_entry_repository, "get_entry") as mock_get:
            mock_get.return_value = {"entry_id": 42, "title": "Great film"}
            result = main.get_general_entry(42)
            mock_get.assert_called_once_with(42)
            self.assertEqual(result["entry"]["entry_id"], 42)

        with patch.object(main.general_entry_repository, "get_entry") as mock_get:
            mock_get.return_value = None
            with self.assertRaises(HTTPException) as ctx:
                main.get_general_entry(999)
            self.assertEqual(ctx.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()

