import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.movie_repository import MovieRepository
from app.movie_service import MovieService
from app.movie_status import MovieStatus
from app.user_movie_repository import UserMovieRepository


class MoviePaginationAndVerdictTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        path = Path(self.temporary_directory.name) / "movies.db"
        database_patch = patch.object(database, "DATABASE_PATH", path)
        database_patch.start()
        self.addCleanup(database_patch.stop)
        initialize_database()
        self.movies = MovieRepository()
        self.users = UserMovieRepository()
        self.service = MovieService(
            movie_repository=self.movies,
            user_repository=self.users,
            tmdb_client=object(),
        )

    def _save_movie(self, tmdb_id: int) -> None:
        self.movies.save_movie({
            "id": tmdb_id,
            "title": f"Movie {tmdb_id:02d}",
            "original_title": None,
            "release_date": None,
            "overview": None,
            "poster_path": None,
            "backdrop_path": None,
            "vote_average": None,
            "original_language": "en",
        })

    def test_status_pages_use_twenty_movies(self) -> None:
        for movie_id in range(1, 26):
            self._save_movie(movie_id)
            self.users.set_status(movie_id, MovieStatus.WATCH_LATER)
        first = self.service.get_movies_by_status_page("watch_later", 1)
        second = self.service.get_movies_by_status_page("watch_later", 2)
        self.assertEqual(len(first["results"]), 20)
        self.assertEqual(len(second["results"]), 5)
        self.assertEqual(first["total_results"], 25)
        self.assertEqual(first["total_pages"], 2)

    def test_verdict_is_a_whole_number_from_one_to_ten(self) -> None:
        self._save_movie(99)
        result = self.service.set_movie_verdict(99, 8)
        self.assertEqual(result["verdict"], 8)
        cleared = self.service.set_movie_verdict(99, None)
        self.assertIsNone(cleared["verdict"])
        with self.assertRaisesRegex(ValueError, "1 to 10"):
            self.service.set_movie_verdict(99, 11)


if __name__ == "__main__":
    unittest.main()
