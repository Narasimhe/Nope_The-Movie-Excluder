import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.movie_metadata_repository import MovieMetadataRepository
from app.movie_repository import MovieRepository
from app.movie_service import MovieService
from app.movie_status import MovieStatus
from app.user_movie_repository import UserMovieRepository


class FakeTMDBClient:
    pass


class LocalKeywordSearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        database_path = (
            Path(self.temporary_directory.name)
            / "local_keyword_search_test.db"
        )
        database_path_patch = patch.object(
            database,
            "DATABASE_PATH",
            database_path,
        )
        database_path_patch.start()
        self.addCleanup(database_path_patch.stop)

        initialize_database()

        self.movie_repository = MovieRepository()
        self.metadata_repository = MovieMetadataRepository()
        self.user_repository = UserMovieRepository()
        self.service = MovieService(
            movie_repository=self.movie_repository,
            user_repository=self.user_repository,
            metadata_repository=self.metadata_repository,
            tmdb_client=FakeTMDBClient(),
        )

        movies = [
            (101, "Iron Man", MovieStatus.WATCHED),
            (102, "Avengers", MovieStatus.WATCH_LATER),
            (103, "Fantastic Four", MovieStatus.EXCLUDED),
            (104, "Arrival", MovieStatus.REWATCH),
        ]

        for tmdb_id, title, status in movies:
            self.movie_repository.save_movie(
                {
                    "id": tmdb_id,
                    "title": title,
                    "original_title": title,
                    "release_date": "2020-01-01",
                    "overview": "Test movie.",
                    "poster_path": None,
                    "backdrop_path": None,
                    "vote_average": 7.0,
                }
            )
            self.user_repository.set_status(tmdb_id, status)

        official_keyword = {
            "id": 180547,
            "name": "Marvel Cinematic Universe",
        }
        self.metadata_repository.replace_tmdb_keywords(
            101,
            [official_keyword],
        )
        self.metadata_repository.replace_tmdb_keywords(
            102,
            [official_keyword],
        )
        self.metadata_repository.add_custom_keyword(102, "Marvel")
        self.metadata_repository.add_custom_keyword(103, "Marvel")
        self.metadata_repository.add_custom_keyword(
            104,
            "first contact",
        )
        self.metadata_repository.replace_movie_genres(
            101,
            [{"id": 878, "name": "Science Fiction"}],
        )

    def test_all_keyword_search_combines_official_and_custom(self) -> None:
        result = self.service.search_local_movies_by_keyword(
            "mArVeL",
            "all",
        )

        self.assertEqual(result["query"], "mArVeL")
        self.assertEqual(result["keyword_type"], "all")
        self.assertEqual(result["matched_keyword_count"], 2)
        self.assertEqual(result["movie_count"], 3)
        self.assertEqual(
            [movie["tmdb_id"] for movie in result["movies"]],
            [102, 103, 101],
        )

        movies_by_id = {
            movie["tmdb_id"]: movie
            for movie in result["movies"]
        }
        self.assertEqual(
            len(movies_by_id[102]["matched_keywords"]),
            2,
        )
        self.assertEqual(
            movies_by_id[102]["user_data"]["status"],
            MovieStatus.WATCH_LATER.value,
        )
        self.assertEqual(
            movies_by_id[101]["genres"][0]["name"],
            "Science Fiction",
        )

    def test_keyword_type_can_limit_the_search(self) -> None:
        custom = self.service.search_local_movies_by_keyword(
            "marvel",
            "custom",
        )
        tmdb = self.service.search_local_movies_by_keyword(
            "marvel",
            "tmdb",
        )

        self.assertEqual(
            [movie["tmdb_id"] for movie in custom["movies"]],
            [102, 103],
        )
        self.assertTrue(
            all(
                keyword["is_custom"]
                for keyword in custom["matched_keywords"]
            )
        )
        self.assertEqual(
            [movie["tmdb_id"] for movie in tmdb["movies"]],
            [102, 101],
        )
        self.assertTrue(
            all(
                not keyword["is_custom"]
                for keyword in tmdb["matched_keywords"]
            )
        )

    def test_search_text_treats_sql_wildcards_as_text(self) -> None:
        result = self.service.search_local_movies_by_keyword("%")

        self.assertEqual(result["movie_count"], 0)

    def test_invalid_local_keyword_search_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            self.service.search_local_movies_by_keyword("   ")

        with self.assertRaisesRegex(ValueError, "all, custom, or tmdb"):
            self.service.search_local_movies_by_keyword(
                "marvel",
                "maybe",
            )


if __name__ == "__main__":
    unittest.main()
