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


class NoTMDBClient:
    def get_movie(self, movie_id: int) -> dict:
        raise AssertionError("The notes tests must remain local.")


class MovieNotesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        database_path = (
            Path(self.temporary_directory.name)
            / "movie_notes_test.db"
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
        self.user_repository = UserMovieRepository()
        self.metadata_repository = MovieMetadataRepository()

        for movie_id, title in (
            (101, "Cold Film"),
            (202, "Warm Film"),
            (303, "Percentage Film"),
        ):
            self.movie_repository.save_movie(
                {
                    "id": movie_id,
                    "title": title,
                    "original_title": title,
                    "release_date": "2020-01-01",
                    "overview": None,
                    "poster_path": None,
                    "backdrop_path": None,
                    "vote_average": 7.0,
                }
            )

        self.user_repository.set_status(
            101,
            MovieStatus.NEW_DISCOVERY,
        )
        self.user_repository.set_status(
            202,
            MovieStatus.WATCHED,
        )
        self.user_repository.set_status(
            303,
            MovieStatus.EXCLUDED,
        )
        self.user_repository.set_notes(
            101,
            "Beautiful cold ambience and quiet streets.",
        )
        self.user_repository.set_notes(
            202,
            "Warm daylight and quick pacing.",
        )
        self.user_repository.set_notes(
            303,
            "A 100% literal observation.",
        )

        self.service = MovieService(
            movie_repository=self.movie_repository,
            user_repository=self.user_repository,
            metadata_repository=self.metadata_repository,
            tmdb_client=NoTMDBClient(),
        )

    def test_notes_search_is_case_insensitive_and_partial(self) -> None:
        matches = self.user_repository.search_notes("COLD ambience")

        self.assertEqual(
            [match["tmdb_id"] for match in matches],
            [101],
        )

    def test_notes_search_comma_separated_multiple_terms(self) -> None:
        matches = self.user_repository.search_notes("cold, streets")
        self.assertEqual(
            [match["tmdb_id"] for match in matches],
            [101],
        )

    def test_notes_search_matches_genre_and_notes(self) -> None:
        self.metadata_repository.replace_movie_genres(
            101, [{"id": 27, "name": "Horror"}]
        )
        matches = self.user_repository.search_notes("streets, Horror")
        self.assertEqual(
            [match["tmdb_id"] for match in matches],
            [101],
        )

    def test_notes_search_treats_wildcards_as_text(self) -> None:
        matches = self.user_repository.search_notes("%")

        self.assertEqual(
            [match["tmdb_id"] for match in matches],
            [303],
        )

    def test_empty_notes_search_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.user_repository.search_notes("   ")

    def test_service_returns_movies_with_personal_data(self) -> None:
        results = self.service.search_movie_notes("quiet streets")

        self.assertEqual(
            [movie["tmdb_id"] for movie in results],
            [101],
        )
        self.assertEqual(
            results[0]["user_data"]["status"],
            MovieStatus.NEW_DISCOVERY.value,
        )
        self.assertIn(
            "cold ambience",
            results[0]["user_data"]["notes"],
        )

    def test_notes_can_be_updated_and_cleared(self) -> None:
        updated = self.service.set_movie_notes(
            101,
            "  Keep this one.  ",
        )
        cleared = self.service.set_movie_notes(101, "   ")

        self.assertEqual(updated["notes"], "Keep this one.")
        self.assertIsNone(cleared["notes"])

    def test_library_search_word_boundary_prevents_mid_word_false_positives(self) -> None:
        self.movie_repository.save_movie(
            {
                "id": 401,
                "title": "Layer Cake",
                "original_title": "Layer Cake",
                "release_date": "2004-10-01",
                "overview": "When a seemingly straight-forward drug deal goes awry against all odds.",
            }
        )
        self.user_repository.set_status(401, MovieStatus.WATCHED)

        self.movie_repository.save_movie(
            {
                "id": 402,
                "title": "A.I. Artificial Intelligence",
                "original_title": "A.I. Artificial Intelligence",
                "release_date": "2001-06-29",
                "overview": "A robotic boy longs to become real.",
            }
        )
        self.user_repository.set_status(402, MovieStatus.WATCHED)

        self.movie_repository.save_movie(
            {
                "id": 403,
                "title": "I Am Mother",
                "original_title": "I Am Mother",
                "release_date": "2019-06-07",
                "overview": "A teenage girl is raised underground by a robot.",
            }
        )
        self.user_repository.set_status(403, MovieStatus.WATCHED)
        self.metadata_repository.add_custom_keyword(403, "artificial intelligence (a.i.)")

        results = self.movie_repository.search_user_library("ai")
        matched_ids = [m["tmdb_id"] for m in results]
        self.assertEqual(matched_ids, [402, 403])
        self.assertNotIn(401, matched_ids)

    def test_library_search_five_tier_hierarchy_and_prefixes(self) -> None:
        # Tier 5: keyword match
        self.movie_repository.save_movie(
            {"id": 505, "title": "Zeta Film", "overview": "A quiet drama."}
        )
        self.user_repository.set_status(505, MovieStatus.WATCHED)
        self.metadata_repository.add_custom_keyword(505, "american dream")

        # Tier 4: personal notes match
        self.movie_repository.save_movie(
            {"id": 504, "title": "Beta Film", "overview": "A coastal story."}
        )
        self.user_repository.set_status(504, MovieStatus.WATCHED)
        self.user_repository.set_notes(504, "Classic american road trip vibe.")

        # Tier 3: TMDB plot blurb match
        self.movie_repository.save_movie(
            {"id": 503, "title": "Alpha Film", "overview": "An american journalist travels abroad."}
        )
        self.user_repository.set_status(503, MovieStatus.WATCHED)

        # Tier 2: Title contains word
        self.movie_repository.save_movie(
            {"id": 502, "title": "American Psycho", "overview": "Wall Street thriller."}
        )
        self.user_repository.set_status(502, MovieStatus.WATCHED)

        # Tier 1: Exact title match
        self.movie_repository.save_movie(
            {"id": 501, "title": "American", "overview": "A standalone story."}
        )
        self.user_repository.set_status(501, MovieStatus.WATCHED)

        all_results = self.movie_repository.search_user_library("american")
        self.assertEqual([m["tmdb_id"] for m in all_results], [501, 502, 503, 504, 505])
        self.assertEqual([m["search_tier"] for m in all_results], [1, 2, 3, 4, 5])

        title_only = self.movie_repository.search_user_library("title: american")
        self.assertEqual([m["tmdb_id"] for m in title_only], [501, 502])

        plot_only = self.movie_repository.search_user_library("plot: american")
        self.assertEqual([m["tmdb_id"] for m in plot_only], [503])

        notes_only = self.movie_repository.search_user_library("notes: american")
        self.assertEqual([m["tmdb_id"] for m in notes_only], [504])

        multi_term_notes = self.movie_repository.search_user_library("classic, road", status="movie-notes")
        self.assertEqual([m["tmdb_id"] for m in multi_term_notes], [504])

        self.movie_repository.save_movie(
            {"id": 506, "title": "Zero Dark Thirty", "overview": "Military procedural drama."}
        )
        self.user_repository.set_status(506, MovieStatus.WATCHED)
        self.user_repository.set_notes(
            506,
            "Grey says:\nZero Dark Thirty (2012) [Drama, Thriller]\nA cold, intensely methodical procedural thriller that relies on rigorous intelligence craft rather than Hollywood sensationalism.",
        )
        zdt_matches = self.movie_repository.search_user_library("grey, zero, intelligent", status="movie-notes")
        self.assertEqual([m["tmdb_id"] for m in zdt_matches], [506])

    def test_movie_notes_shelf_double_select_status_filter(self) -> None:
        watched_notes = self.movie_repository.search_user_library("", status="movie-notes:watched")
        self.assertEqual([m["tmdb_id"] for m in watched_notes], [202])

        nope_notes = self.movie_repository.search_user_library("", status="movie-notes:excluded")
        self.assertEqual([m["tmdb_id"] for m in nope_notes], [303])


if __name__ == "__main__":
    unittest.main()
