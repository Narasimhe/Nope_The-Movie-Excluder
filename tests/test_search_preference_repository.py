import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.advanced_filters import AdvancedMovieFilters
from app.database import initialize_database
from app.search_preference_repository import (
    SearchPreferenceRepository,
)


class SearchPreferenceRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        database_path = (
            Path(self.temporary_directory.name)
            / "search_preferences_test.db"
        )
        database_path_patch = patch.object(
            database,
            "DATABASE_PATH",
            database_path,
        )
        database_path_patch.start()
        self.addCleanup(database_path_patch.stop)

        initialize_database()
        self.repository = SearchPreferenceRepository()

    def test_search_preferences_table_is_created(self) -> None:
        with database.get_connection() as connection:
            row = connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = 'search_preferences'
                """
            ).fetchone()

        self.assertIsNotNone(row)

    def test_preference_saves_validated_filters(self) -> None:
        preference = self.repository.create_preference(
            "American Sci-Fi",
            {
                "include_genre_ids": [878],
                "include_actor_ids": [31],
                "include_director_ids": [525],
                "include_company_ids": [9993],
                "exclude_company_ids": [420],
                "include_origin_countries": ["us"],
                "exclude_origin_countries": ["in", "pk"],
                "minimum_rating": 7,
            },
        )

        loaded = self.repository.get_preference(
            preference["preference_id"]
        )

        self.assertEqual(loaded["name"], "American Sci-Fi")
        self.assertEqual(
            loaded["filters"]["include_origin_countries"],
            ["US"],
        )
        self.assertEqual(
            loaded["filters"]["exclude_origin_countries"],
            ["IN", "PK"],
        )
        self.assertEqual(
            loaded["filters"]["include_genre_ids"],
            [878],
        )
        self.assertEqual(
            loaded["filters"]["include_actor_ids"],
            [31],
        )
        self.assertEqual(
            loaded["filters"]["include_director_ids"],
            [525],
        )
        self.assertEqual(
            loaded["filters"]["include_company_ids"],
            [9993],
        )

    def test_preference_accepts_filter_model(self) -> None:
        filters = AdvancedMovieFilters(
            include_original_languages=["en"],
            minimum_vote_count=100,
        )

        preference = self.repository.create_preference(
            "English Movies",
            filters,
        )

        self.assertEqual(
            preference["filters"]["minimum_vote_count"],
            100,
        )

    def test_preference_remembers_super_advanced_filters(self) -> None:
        preference = self.repository.create_preference(
            "Unwatched English",
            {"include_original_languages": ["en"]},
            personal_filters={
                "included_statuses": ["new_discovery"],
                "include_untracked": True,
                "notes_query": "cold ambience",
                "favorite_only": False,
            },
        )

        self.assertEqual(
            preference["personal_filters"]["included_statuses"],
            ["new_discovery"],
        )
        self.assertEqual(
            preference["personal_filters"]["notes_query"],
            "cold ambience",
        )

    def test_preference_can_be_updated(self) -> None:
        created = self.repository.create_preference(
            "American Movies",
            {"include_origin_countries": ["US"]},
            is_default=True,
        )

        updated = self.repository.update_preference(
            created["preference_id"],
            "American Science Fiction",
            {
                "include_origin_countries": ["US"],
                "include_genre_ids": [878],
            },
        )

        self.assertEqual(
            updated["name"],
            "American Science Fiction",
        )
        self.assertEqual(
            updated["filters"]["include_genre_ids"],
            [878],
        )
        self.assertTrue(updated["is_default"])

    def test_only_one_preference_can_be_default(self) -> None:
        first = self.repository.create_preference(
            "American Movies",
            {"include_origin_countries": ["US"]},
            is_default=True,
        )
        second = self.repository.create_preference(
            "British Movies",
            {"include_origin_countries": ["GB"]},
        )

        selected = self.repository.set_default(
            second["preference_id"]
        )
        previous = self.repository.get_preference(
            first["preference_id"]
        )

        self.assertTrue(selected["is_default"])
        self.assertFalse(previous["is_default"])
        self.assertEqual(
            self.repository.get_default_preference()[
                "preference_id"
            ],
            second["preference_id"],
        )

    def test_preferences_are_listed_by_name(self) -> None:
        self.repository.create_preference(
            "Thrillers",
            {"include_genre_ids": [53]},
        )
        self.repository.create_preference(
            "American Movies",
            {"include_origin_countries": ["US"]},
        )

        preferences = self.repository.list_preferences()

        self.assertEqual(
            [preference["name"] for preference in preferences],
            ["American Movies", "Thrillers"],
        )

    def test_duplicate_names_are_rejected_case_insensitively(self) -> None:
        self.repository.create_preference(
            "American Movies",
            {"include_origin_countries": ["US"]},
        )

        with self.assertRaisesRegex(
            ValueError,
            "already exists",
        ):
            self.repository.create_preference(
                "american movies",
                {"include_origin_countries": ["GB"]},
            )

    def test_invalid_filters_are_not_saved(self) -> None:
        with self.assertRaises(ValueError):
            self.repository.create_preference(
                "Broken Preference",
                {
                    "include_origin_countries": ["IN"],
                    "exclude_origin_countries": ["IN"],
                },
            )

        self.assertEqual(self.repository.list_preferences(), [])

    def test_preference_can_be_deleted(self) -> None:
        preference = self.repository.create_preference(
            "Temporary",
            {},
        )

        removed = self.repository.delete_preference(
            preference["preference_id"]
        )

        self.assertTrue(removed)
        self.assertIsNone(
            self.repository.get_preference(
                preference["preference_id"]
            )
        )


if __name__ == "__main__":
    unittest.main()
