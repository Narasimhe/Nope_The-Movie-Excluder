import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class FakeMovieService:
    def __init__(self) -> None:
        self.added: tuple[int, str] | None = None
        self.removed: tuple[int, int] | None = None
        self.remove_result = True
        self.deleted_keyword: dict | None = {
            "keyword_id": 51,
            "name": "cold ambience",
            "is_custom": True,
            "affected_movie_count": 2,
        }

    def add_custom_keyword(
        self,
        tmdb_id: int,
        name: str,
    ) -> dict:
        if not name.strip():
            raise ValueError("Custom keyword name cannot be empty.")

        self.added = (tmdb_id, name)
        return {
            "keyword_id": 51,
            "tmdb_keyword_id": None,
            "name": name,
            "is_custom": True,
            "position": None,
        }

    def remove_custom_keyword(
        self,
        tmdb_id: int,
        keyword_id: int,
    ) -> bool:
        self.removed = (tmdb_id, keyword_id)
        return self.remove_result

    def delete_custom_keyword(
        self,
        keyword_id: int,
    ) -> dict | None:
        if self.deleted_keyword is None:
            return None

        return {
            **self.deleted_keyword,
            "keyword_id": keyword_id,
        }


class CustomKeywordEndpointTests(unittest.TestCase):
    def test_custom_keyword_routes_are_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn(
            "/movies/{tmdb_id}/keywords/custom",
            route_paths,
        )
        self.assertIn(
            "/movies/{tmdb_id}/keywords/custom/{keyword_id}",
            route_paths,
        )
        self.assertIn(
            "/keywords/custom/{keyword_id}",
            route_paths,
        )

    def test_add_custom_keyword(self) -> None:
        fake_service = FakeMovieService()
        request = main.CustomKeywordRequest(name="cold ambience")

        with patch.object(main, "movie_service", fake_service):
            result = main.add_custom_keyword(603, request)

        self.assertEqual(
            fake_service.added,
            (603, "cold ambience"),
        )
        self.assertTrue(result["keyword"]["is_custom"])

    def test_blank_custom_keyword_returns_400(self) -> None:
        fake_service = FakeMovieService()
        request = main.CustomKeywordRequest(name="   ")

        with patch.object(main, "movie_service", fake_service):
            with self.assertRaises(HTTPException) as context:
                main.add_custom_keyword(603, request)

        self.assertEqual(context.exception.status_code, 400)

    def test_remove_custom_keyword(self) -> None:
        fake_service = FakeMovieService()

        with patch.object(main, "movie_service", fake_service):
            result = main.remove_custom_keyword(603, 51)

        self.assertEqual(fake_service.removed, (603, 51))
        self.assertEqual(
            result["message"],
            "Custom keyword removed from this movie",
        )

    def test_missing_custom_keyword_returns_404(self) -> None:
        fake_service = FakeMovieService()
        fake_service.remove_result = False

        with patch.object(main, "movie_service", fake_service):
            with self.assertRaises(HTTPException) as context:
                main.remove_custom_keyword(603, 999)

        self.assertEqual(context.exception.status_code, 404)

    def test_delete_custom_keyword_from_every_movie(self) -> None:
        fake_service = FakeMovieService()

        with patch.object(main, "movie_service", fake_service):
            result = main.delete_custom_keyword(51)

        self.assertEqual(
            result["deleted_keyword"]["affected_movie_count"],
            2,
        )
        self.assertEqual(
            result["message"],
            "Custom keyword deleted from every movie",
        )

    def test_missing_global_custom_keyword_returns_404(self) -> None:
        fake_service = FakeMovieService()
        fake_service.deleted_keyword = None

        with patch.object(main, "movie_service", fake_service):
            with self.assertRaises(HTTPException) as context:
                main.delete_custom_keyword(999)

        self.assertEqual(context.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
