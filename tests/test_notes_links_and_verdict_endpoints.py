import unittest
from unittest.mock import patch

from app import main


class FakeEntryRepository:
    def __init__(self) -> None:
        self.created = None

    def create_entry(self, entry_type, title, body, url, tags):
        self.created = (entry_type, title, body, url, tags)
        return {
            "entry_id": 1,
            "entry_type": entry_type,
            "title": title,
            "body": body,
            "url": url,
            "tags": tags,
        }


class FakeVerdictService:
    def set_movie_verdict(self, tmdb_id, verdict):
        return {"tmdb_id": tmdb_id, "verdict": verdict}


class NotesLinksAndVerdictEndpointTests(unittest.TestCase):
    def test_new_routes_are_registered(self) -> None:
        routes = {route.path for route in main.app.routes}
        self.assertIn("/entries", routes)
        self.assertIn("/entries/{entry_id}", routes)
        self.assertIn("/search-state", routes)
        self.assertIn("/movies/{tmdb_id}/verdict", routes)

    def test_general_entry_can_be_created(self) -> None:
        repository = FakeEntryRepository()
        request = main.GeneralEntryRequest(
            entry_type="link",
            title="Slow-burn site",
            body="Useful source",
            url="example.com",
            tags=["slow burn"],
        )
        with patch.object(main, "general_entry_repository", repository):
            result = main.create_general_entry(request)
        self.assertEqual(
            repository.created,
            ("link", "Slow-burn site", "Useful source", "example.com", ["slow burn"]),
        )
        self.assertEqual(result["entry"]["entry_id"], 1)

    def test_movie_verdict_can_be_saved(self) -> None:
        request = main.MovieVerdictRequest(verdict=9)
        with patch.object(main, "movie_service", FakeVerdictService()):
            result = main.set_movie_verdict(603, request)
        self.assertEqual(result["user_movie_data"]["verdict"], 9)


if __name__ == "__main__":
    unittest.main()
