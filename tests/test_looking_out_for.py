from datetime import date
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.looking_out_for_repository import LookingOutForRepository
from app.movie_service import MovieService
from app.movie_status import MovieStatus
from app.user_movie_repository import UserMovieRepository


class FutureTMDBClient:
    def __init__(self, release_date: str = "2027-07-01") -> None:
        self.release_date = release_date

    def get_movie(self, movie_id: int) -> dict:
        return {
            "id": movie_id,
            "title": "Future Film",
            "original_title": "Future Film",
            "release_date": self.release_date,
            "overview": "Coming later.",
            "poster_path": "/future.jpg",
            "backdrop_path": None,
            "vote_average": 0,
            "original_language": "en",
            "genres": [],
            "keywords": {"keywords": []},
            "credits": {"crew": [], "cast": []},
        }

    def get_movie_recommendations(self, movie_id: int) -> dict:
        return {"results": []}

    def get_similar_movies(self, movie_id: int) -> dict:
        return {"results": []}


class LookingOutForTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        path = Path(self.temporary_directory.name) / "upcoming.db"
        database_patch = patch.object(database, "DATABASE_PATH", path)
        database_patch.start()
        self.addCleanup(database_patch.stop)
        initialize_database()
        self.repository = LookingOutForRepository()
        self.user_repository = UserMovieRepository()
        self.service = MovieService(
            user_repository=self.user_repository,
            looking_out_for_repository=self.repository,
            tmdb_client=FutureTMDBClient(),
        )

    def test_future_movie_tracking_is_independent_of_main_status(self) -> None:
        with patch("app.movie_service.local_today", return_value=date(2026, 8, 2)):
            tracked = self.service.add_to_looking_out_for(1001)
            movie = self.service.get_movie(1001)

        self.assertEqual(tracked["release_date"], "2027-07-01")
        self.assertTrue(movie["is_looking_out_for"])
        self.assertIsNone(self.user_repository.get_user_movie_data(1001))

    def test_tracked_movie_is_hidden_from_new_discovery_shelf(self) -> None:
        with patch("app.movie_service.local_today", return_value=date(2026, 8, 2)):
            self.service.add_to_looking_out_for(1004)
        self.user_repository.set_status(1004, MovieStatus.NEW_DISCOVERY)

        hidden = self.service.get_movies_by_status_page(
            MovieStatus.NEW_DISCOVERY,
        )
        self.assertEqual(hidden["total_results"], 0)
        self.assertEqual(
            self.user_repository.get_user_movie_data(1004)["status"],
            MovieStatus.NEW_DISCOVERY.value,
        )

        self.service.remove_from_looking_out_for(1004)
        visible_again = self.service.get_movies_by_status_page(
            MovieStatus.NEW_DISCOVERY,
        )
        self.assertEqual(visible_again["total_results"], 1)

    def test_released_movie_cannot_be_newly_tracked(self) -> None:
        service = MovieService(tmdb_client=FutureTMDBClient("2026-08-01"))
        with patch("app.movie_service.local_today", return_value=date(2026, 8, 2)):
            with self.assertRaisesRegex(ValueError, "future"):
                service.add_to_looking_out_for(1002)

    def test_released_tracked_movie_can_move_to_watch_later(self) -> None:
        with patch("app.movie_service.local_today", return_value=date(2026, 8, 2)):
            self.service.add_to_looking_out_for(1003)
            self.repository.update_release_date(1003, "2026-08-01")
            user_data = self.service.move_looking_out_for_to_watch_later(1003)

        self.assertEqual(user_data["status"], MovieStatus.WATCH_LATER.value)
        self.assertIsNone(self.repository.get(1003))

    def test_release_alert_preference_is_persistent(self) -> None:
        self.assertTrue(self.service.get_release_alerts_enabled())
        self.assertFalse(self.service.set_release_alerts_enabled(False))
        self.assertFalse(self.service.get_release_alerts_enabled())

    def test_release_alert_count_covers_movies_on_every_page(self) -> None:
        for movie_id in range(2000, 2021):
            self.service.movie_repository.save_movie({
                "id": movie_id,
                "title": f"Future Film {movie_id}",
                "release_date": "2028-01-01",
            })
            self.repository.add(movie_id, "2028-01-01")

        self.repository.update_release_date(2000, "2026-08-01")
        self.repository.update_release_date(2001, "2026-08-02")
        self.repository.update_release_date(2002, "2026-08-05")

        with patch("app.movie_service.local_today", return_value=date(2026, 8, 2)):
            first_page = self.service.get_looking_out_for_movies(1)

        self.assertEqual(first_page["total_pages"], 2)
        self.assertEqual(first_page["alert_count"], 3)
        self.assertEqual(
            first_page["alert_counts"],
            {"released": 1, "today": 1, "soon": 1},
        )


if __name__ == "__main__":
    unittest.main()
