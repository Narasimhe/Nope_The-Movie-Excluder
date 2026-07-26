import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class FakeFavoriteService:
    def __init__(self) -> None:
        self.updated: tuple[int, bool] | None = None

    def set_movie_favorite(
        self,
        tmdb_id: int,
        is_favorite: bool,
    ) -> dict:
        if tmdb_id == 303 and is_favorite:
            raise ValueError(
                "Only watched or rewatch movies can be favorited."
            )

        self.updated = (tmdb_id, is_favorite)
        return {
            "tmdb_id": tmdb_id,
            "status": "watched",
            "notes": "A favorite.",
            "is_favorite": is_favorite,
        }

    def get_favorite_movies(self) -> list[dict]:
        return [
            {
                "tmdb_id": 101,
                "title": "Favorite Movie",
                "user_data": {
                    "is_favorite": True,
                },
            }
        ]


class FavoriteEndpointTests(unittest.TestCase):
    def test_favorite_routes_are_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/movies/{tmdb_id}/favorite", route_paths)
        self.assertIn("/movies/favorites", route_paths)

    def test_movie_can_be_favorited(self) -> None:
        service = FakeFavoriteService()
        request = main.FavoriteRequest(is_favorite=True)

        with patch.object(main, "movie_service", service):
            result = main.set_movie_favorite(101, request)

        self.assertEqual(service.updated, (101, True))
        self.assertEqual(
            result["message"],
            "Movie added to favorites",
        )
        self.assertTrue(
            result["user_movie_data"]["is_favorite"]
        )

    def test_movie_can_be_unfavorited(self) -> None:
        service = FakeFavoriteService()
        request = main.FavoriteRequest(is_favorite=False)

        with patch.object(main, "movie_service", service):
            result = main.set_movie_favorite(101, request)

        self.assertEqual(service.updated, (101, False))
        self.assertEqual(
            result["message"],
            "Movie removed from favorites",
        )

    def test_favorites_can_be_listed(self) -> None:
        service = FakeFavoriteService()

        with patch.object(main, "movie_service", service):
            result = main.get_favorite_movies()

        self.assertEqual(result[0]["tmdb_id"], 101)
        self.assertTrue(result[0]["user_data"]["is_favorite"])

    def test_unwatched_favorite_attempt_returns_400(self) -> None:
        service = FakeFavoriteService()
        request = main.FavoriteRequest(is_favorite=True)

        with patch.object(main, "movie_service", service):
            with self.assertRaises(HTTPException) as context:
                main.set_movie_favorite(303, request)

        self.assertEqual(context.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
