import unittest
from unittest.mock import patch

from app import main
from app.mdblist_client import MDBListClient


class MDBListRatingsTests(unittest.TestCase):
    def test_ratings_route_is_registered(self) -> None:
        route_paths = {route.path for route in main.app.routes}
        self.assertIn("/movies/{tmdb_id}/ratings", route_paths)

    def test_extract_ratings_parses_all_sources(self) -> None:
        payload = {
            "title": "Fight Club",
            "year": 1999,
            "ratings": [
                {"source": "imdb", "value": 8.8, "votes": 2679431},
                {"source": "metacritic", "value": 67},
                {"source": "tomatoes", "value": 81},
                {"source": "tomatoesaudience", "value": 96},
                {"source": "letterboxd", "value": 4.3},
            ],
        }

        parsed = MDBListClient._extract_ratings(payload)
        self.assertEqual(parsed["tomatoes"], 81)
        self.assertEqual(parsed["popcorn"], 96)
        self.assertEqual(parsed["imdb"], 8.8)
        self.assertEqual(parsed["imdb_votes"], 2679431)
        self.assertEqual(parsed["letterboxd"], 4.3)
        self.assertEqual(parsed["metacritic"], 67)

    def test_extract_ratings_handles_missing_sources_gracefully(self) -> None:
        payload = {
            "title": "Obscure Film",
            "year": 1950,
            "ratings": [
                {"source": "imdb", "value": 7.2},
            ],
        }

        parsed = MDBListClient._extract_ratings(payload)
        self.assertIsNone(parsed["tomatoes"])
        self.assertIsNone(parsed["popcorn"])
        self.assertEqual(parsed["imdb"], 7.2)
        self.assertIsNone(parsed["imdb_votes"])
        self.assertIsNone(parsed["letterboxd"])
        self.assertIsNone(parsed["metacritic"])

    def test_get_movie_ratings_endpoint_returns_data(self) -> None:
        mock_ratings = {
            "tomatoes": 93,
            "popcorn": 94,
            "imdb": 8.5,
            "imdb_votes": 1300000,
            "letterboxd": 4.3,
            "metacritic": 87,
        }

        with patch.object(main.mdblist_client, "get_ratings", return_value=mock_ratings) as mock_get:
            response = main.get_movie_ratings(550, force_refresh=True)
            mock_get.assert_called_once_with(550, force_refresh=True)

        self.assertEqual(response["tmdb_id"], 550)
        self.assertEqual(response["ratings"], mock_ratings)
