import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class FakeMovieNoteService:
    def __init__(self) -> None:
        self.saved: tuple[int, str | None] | None = None
        self.query: str | None = None

    def set_movie_notes(
        self,
        tmdb_id: int,
        notes: str | None,
    ) -> dict:
        self.saved = (tmdb_id, notes)
        return {
            "tmdb_id": tmdb_id,
            "status": "new_discovery",
            "notes": notes,
        }

    def search_movie_notes(self, query: str) -> list[dict]:
        if not query.strip():
            raise ValueError("Notes search query cannot be empty.")

        self.query = query
        return [
            {
                "tmdb_id": 101,
                "title": "Arrival",
                "user_data": {
                    "notes": "Beautiful cold ambience.",
                },
            }
        ]


class MovieNoteEndpointTests(unittest.TestCase):
    def test_note_routes_are_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/movies/{tmdb_id}/notes", route_paths)
        self.assertIn("/movies/notes/search", route_paths)

    def test_notes_can_be_saved(self) -> None:
        service = FakeMovieNoteService()
        request = main.MovieNotesRequest(
            notes="Beautiful cold ambience."
        )

        with patch.object(main, "movie_service", service):
            result = main.set_movie_notes(101, request)

        self.assertEqual(
            service.saved,
            (101, "Beautiful cold ambience."),
        )
        self.assertEqual(
            result["user_movie_data"]["tmdb_id"],
            101,
        )

    def test_notes_can_be_searched(self) -> None:
        service = FakeMovieNoteService()

        with patch.object(main, "movie_service", service):
            result = main.search_movie_notes("cold ambience")

        self.assertEqual(service.query, "cold ambience")
        self.assertEqual(result[0]["tmdb_id"], 101)

    def test_empty_note_search_returns_400(self) -> None:
        service = FakeMovieNoteService()

        with patch.object(main, "movie_service", service):
            with self.assertRaises(HTTPException) as context:
                main.search_movie_notes("   ")

        self.assertEqual(context.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
