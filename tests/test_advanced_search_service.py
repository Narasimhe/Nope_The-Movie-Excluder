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
        self.detail_calls: list[int] = []

    def discover_movies(self, filters, page: int = 1) -> dict:
        self.discover_call = {
            "filters": filters,
            "page": page,
        }
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


class AdvancedSearchServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmdb_client = FakeTMDBClient()
        self.preference_repository = FakePreferenceRepository()
        self.service = AdvancedSearchService(
            tmdb_client=self.tmdb_client,
            preference_repository=self.preference_repository,
        )

    def test_default_preference_runs_advanced_search(self) -> None:
        result = self.service.search(page=2)

        self.assertEqual(
            result["preference"]["preference_id"],
            1,
        )
        self.assertEqual(
            self.tmdb_client.discover_call["page"],
            2,
        )
        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [101],
        )
        self.assertEqual(result["candidate_count"], 3)
        self.assertEqual(result["result_count"], 1)
        self.assertEqual(result["country_detail_lookups"], 3)

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

    def test_missing_selected_preference_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            LookupError,
            "not found",
        ):
            self.service.search(preference_id=999)

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
