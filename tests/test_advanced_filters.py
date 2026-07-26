import unittest

from app.advanced_filters import (
    AdvancedMovieFilters,
    FilterLogic,
)


class AdvancedMovieFiltersTests(unittest.TestCase):
    def test_builds_tmdb_params_with_and_or_logic(self) -> None:
        filters = AdvancedMovieFilters(
            include_genre_ids=[878, 53],
            exclude_genre_ids=[27, 10749],
            genre_logic="or",
            include_keyword_ids=[310, 456],
            exclude_keyword_ids=[999],
            keyword_logic="and",
            include_original_languages=["EN"],
            include_origin_countries=["us"],
            minimum_rating=7,
            maximum_rating=9.5,
            minimum_vote_count=100,
            release_year_from=2010,
            release_year_to=2026,
            runtime_min=80,
            runtime_max=160,
            sort_by="vote_average.desc",
        )

        params = filters.to_tmdb_params()

        self.assertEqual(params["with_genres"], "878|53")
        self.assertEqual(params["without_genres"], "27|10749")
        self.assertEqual(params["with_keywords"], "310,456")
        self.assertEqual(params["without_keywords"], "999")
        self.assertEqual(params["with_original_language"], "en")
        self.assertEqual(params["with_origin_country"], "US")
        self.assertEqual(params["vote_average.gte"], 7)
        self.assertEqual(params["vote_average.lte"], 9.5)
        self.assertEqual(params["vote_count.gte"], 100)
        self.assertEqual(
            params["primary_release_date.gte"],
            "2010-01-01",
        )
        self.assertEqual(
            params["primary_release_date.lte"],
            "2026-12-31",
        )
        self.assertEqual(params["with_runtime.gte"], 80)
        self.assertEqual(params["with_runtime.lte"], 160)

    def test_multiple_languages_and_countries_use_local_rules(self) -> None:
        filters = AdvancedMovieFilters(
            include_original_languages=["en", "fr"],
            exclude_original_languages=["hi", "te"],
            include_origin_countries=["US", "GB"],
            exclude_origin_countries=["IN", "PK"],
            country_logic=FilterLogic.OR,
        )

        params = filters.to_tmdb_params()

        self.assertNotIn("with_original_language", params)
        self.assertNotIn("with_origin_country", params)

        matching_movie = {
            "original_language": "en",
            "origin_country": ["US"],
        }
        excluded_movie = {
            "original_language": "en",
            "origin_country": ["US", "IN"],
        }

        self.assertTrue(
            filters.matches_local_rules(matching_movie)
        )
        self.assertFalse(
            filters.matches_local_rules(excluded_movie)
        )

    def test_country_and_logic_requires_every_country(self) -> None:
        filters = AdvancedMovieFilters(
            include_origin_countries=["US", "GB"],
            country_logic="and",
        )

        self.assertTrue(
            filters.matches_local_rules(
                {"origin_country": ["US", "GB"]}
            )
        )
        self.assertFalse(
            filters.matches_local_rules(
                {"origin_country": ["US"]}
            )
        )

    def test_production_country_details_are_supported(self) -> None:
        filters = AdvancedMovieFilters(
            exclude_origin_countries=["IN", "PK"],
        )

        movie = {
            "production_countries": [
                {"iso_3166_1": "US", "name": "United States"},
                {"iso_3166_1": "IN", "name": "India"},
            ]
        }

        self.assertFalse(filters.matches_local_rules(movie))

    def test_missing_country_data_is_detected(self) -> None:
        filters = AdvancedMovieFilters(
            exclude_origin_countries=["IN"],
        )
        movie = {"id": 603, "title": "The Matrix"}

        self.assertTrue(filters.needs_country_details(movie))
        self.assertFalse(filters.matches_local_rules(movie))

    def test_filter_config_is_ready_for_preference_storage(self) -> None:
        filters = AdvancedMovieFilters(
            include_genre_ids=[878],
            exclude_origin_countries=["in", "pk"],
            country_logic="or",
            minimum_rating=7,
        )

        saved = filters.to_dict()
        restored = AdvancedMovieFilters(**saved)

        self.assertEqual(restored.to_dict(), saved)

    def test_invalid_filter_combinations_are_rejected(self) -> None:
        invalid_filters = [
            {"minimum_rating": 11},
            {"minimum_rating": 8, "maximum_rating": 7},
            {"runtime_min": 160, "runtime_max": 80},
            {
                "include_origin_countries": ["IN"],
                "exclude_origin_countries": ["in"],
            },
            {"genre_logic": "maybe"},
            {"sort_by": "random.desc"},
        ]

        for values in invalid_filters:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    AdvancedMovieFilters(**values)


if __name__ == "__main__":
    unittest.main()
