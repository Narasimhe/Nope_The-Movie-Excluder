import unittest

from app.advanced_search_service import AdvancedSearchService


class FakePreferenceRepository:
    def __init__(self) -> None:
        self.default_preference = self._preference(1)
        self.preferences = {
            1: self.default_preference,
            2: self._preference(
                2,
                filters={
                    "include_original_languages": ["en"],
                    "minimum_rating": 7,
                },
            ),
            3: self._preference(
                3,
                filters={
                    "include_director_ids": [525],
                },
            ),
        }

    @staticmethod
    def _preference(
        preference_id: int,
        filters: dict | None = None,
    ) -> dict:
        return {
            "preference_id": preference_id,
            "name": f"Preference {preference_id}",
            "filters": filters
            or {
                "include_original_languages": ["en"],
                "include_origin_countries": ["US"],
                "exclude_origin_countries": ["IN", "PK"],
                "minimum_rating": 7,
            },
            "is_default": preference_id == 1,
        }

    def get_default_preference(self) -> dict | None:
        return self.default_preference

    def get_preference(self, preference_id: int) -> dict | None:
        return self.preferences.get(preference_id)


class FakeTMDBClient:
    def __init__(self) -> None:
        self.discover_call: dict | None = None
        self.discover_pages: list[int] = []
        self.detail_calls: list[int] = []

    def discover_movies(self, filters, page: int = 1) -> dict:
        self.discover_call = {
            "filters": filters,
            "page": page,
        }
        self.discover_pages.append(page)
        return {
            "page": page,
            "total_pages": 5,
            "total_results": 81,
            "results": [
                {
                    "id": 101,
                    "title": "American Film",
                    "original_language": "en",
                },
                {
                    "id": 202,
                    "title": "American-Indian Co-production",
                    "original_language": "en",
                },
                {
                    "id": 303,
                    "title": "Different Language",
                    "original_language": "hi",
                },
            ],
        }

    def get_movie_filter_details(self, movie_id: int) -> dict:
        self.detail_calls.append(movie_id)

        countries = {
            101: {
                "origin_country": ["US"],
                "production_countries": [],
            },
            202: {
                "origin_country": ["US"],
                "production_countries": [
                    {"iso_3166_1": "IN", "name": "India"}
                ],
            },
            303: {
                "origin_country": ["US"],
                "production_countries": [],
            },
        }
        return countries[movie_id]

    def get_person_movie_credits(self, person_id: int) -> dict:
        self.asserted_person_id = person_id
        return {
            "id": person_id,
            "crew": [
                {
                    "id": 101,
                    "title": "American Film",
                    "job": "Director",
                },
                {
                    "id": 202,
                    "title": "American-Indian Co-production",
                    "job": "Producer",
                },
                {
                    "id": 303,
                    "title": "Different Language",
                    "job": "director",
                },
            ],
        }


class AdvancedSearchServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmdb_client = FakeTMDBClient()
        self.preference_repository = FakePreferenceRepository()
        self.service = AdvancedSearchService(
            tmdb_client=self.tmdb_client,
            preference_repository=self.preference_repository,
        )

    def test_default_preference_runs_advanced_search(self) -> None:
        result = self.service.search(page=1)

        self.assertEqual(
            result["preference"]["preference_id"],
            1,
        )
        self.assertEqual(self.tmdb_client.discover_pages, [1, 2, 3, 4, 5])
        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [101],
        )
        self.assertEqual(result["candidate_count"], 3)
        self.assertEqual(result["result_count"], 1)
        self.assertEqual(result["country_detail_lookups"], 3)
        self.assertTrue(result["pagination_exact"])
        self.assertEqual(result["tmdb_total_pages"], 1)
        self.assertEqual(result["tmdb_total_results"], 1)

    def test_selected_preference_is_used(self) -> None:
        result = self.service.search(
            preference_id=2,
            page=1,
        )

        self.assertEqual(
            result["preference"]["preference_id"],
            2,
        )
        self.assertEqual(result["country_detail_lookups"], 0)
        self.assertEqual(self.tmdb_client.detail_calls, [])

    def test_direct_filters_work_without_a_saved_preference(self) -> None:
        self.preference_repository.default_preference = None

        result = self.service.search(
            filters={"include_original_languages": ["en"]},
        )

        self.assertIsNone(result["preference"]["preference_id"])
        self.assertEqual(result["preference"]["name"], "Unsaved search")
        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [101, 202],
        )

    def test_missing_selected_preference_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            LookupError,
            "not found",
        ):
            self.service.search(preference_id=999)

    def test_director_filter_uses_exact_director_credits(self) -> None:
        result = self.service.search(preference_id=3)

        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [101, 303],
        )
        self.assertEqual(result["director_credit_lookups"], 1)
        self.assertEqual(self.tmdb_client.asserted_person_id, 525)
        self.assertTrue(result["pagination_exact"])
        self.assertEqual(result["tmdb_total_pages"], 1)
        self.assertEqual(result["tmdb_total_results"], 2)
        self.assertEqual(result["source_pages_scanned"], 5)

    def test_broad_post_filtered_search_does_not_claim_raw_totals(self) -> None:
        discover = self.tmdb_client.discover_movies

        def broad_discover(filters, page=1):
            response = discover(filters, page)
            response["total_pages"] = 51
            response["total_results"] = 1001
            return response

        self.tmdb_client.discover_movies = broad_discover
        result = self.service.search(
            page=2,
            filters={"exclude_original_languages": ["fr"]},
        )

        self.assertFalse(result["pagination_exact"])
        self.assertIsNone(result["tmdb_total_pages"])
        self.assertIsNone(result["tmdb_total_results"])
        self.assertEqual(result["raw_tmdb_total_pages"], 51)
        self.assertTrue(result["has_next_page"])

    def test_missing_default_preference_is_rejected(self) -> None:
        self.preference_repository.default_preference = None

        with self.assertRaisesRegex(
            LookupError,
            "No default",
        ):
            self.service.search()

    def test_invalid_page_is_rejected_before_tmdb_call(self) -> None:
        with self.assertRaises(ValueError):
            self.service.search(page=0)

        self.assertIsNone(self.tmdb_client.discover_call)


if __name__ == "__main__":
    unittest.main()
