import unittest

from app.movie_status import MovieStatus
from app.super_advanced_search_service import (
    SuperAdvancedSearchService,
)


class FakePreferenceRepository:
    def __init__(self) -> None:
        self.preference = {
            "preference_id": 1,
            "name": "American Sci-Fi",
            "filters": {
                "include_original_languages": ["en"],
                "include_origin_countries": ["US"],
                "exclude_origin_countries": ["IN", "PK"],
                "minimum_rating": 7,
            },
            "is_default": True,
        }

    def get_default_preference(self) -> dict:
        return self.preference

    def get_preference(self, preference_id: int) -> dict | None:
        if preference_id == 1:
            return self.preference
        return None


class FakeUserMovieRepository:
    def __init__(self) -> None:
        self.requested_ids: list[int] | None = None
        self.user_data = {
            202: {
                "tmdb_id": 202,
                "status": MovieStatus.NEW_DISCOVERY.value,
                "notes": "Cold ambience and quiet pacing.",
            },
            303: {
                "tmdb_id": 303,
                "status": MovieStatus.WATCH_LATER.value,
                "notes": "Bright and energetic.",
            },
            404: {
                "tmdb_id": 404,
                "status": MovieStatus.WATCHED.value,
                "notes": "Cold ambience, already watched.",
            },
            505: {
                "tmdb_id": 505,
                "status": MovieStatus.REWATCH.value,
                "notes": None,
            },
            606: {
                "tmdb_id": 606,
                "status": MovieStatus.EXCLUDED.value,
                "notes": "Not interested.",
            },
        }

    def get_user_movie_data_bulk(
        self,
        tmdb_ids: list[int],
    ) -> dict[int, dict]:
        self.requested_ids = tmdb_ids
        return {
            tmdb_id: self.user_data[tmdb_id]
            for tmdb_id in tmdb_ids
            if tmdb_id in self.user_data
        }


class FakeTMDBClient:
    def __init__(self) -> None:
        self.discover_called = False
        self.detail_calls: list[int] = []

    def discover_movies(self, filters, page: int = 1) -> dict:
        self.discover_called = True
        return {
            "page": page,
            "total_pages": 3,
            "total_results": 60,
            "results": [
                {
                    "id": movie_id,
                    "title": f"Movie {movie_id}",
                    "original_language": "en",
                }
                for movie_id in (101, 202, 303, 404, 505, 606)
            ],
        }

    def get_movie_filter_details(self, movie_id: int) -> dict:
        self.detail_calls.append(movie_id)

        if movie_id == 303:
            return {
                "origin_country": ["US"],
                "production_countries": [
                    {"iso_3166_1": "IN", "name": "India"}
                ],
            }

        return {
            "origin_country": ["US"],
            "production_countries": [],
        }

    def get_person_movie_credits(self, person_id: int) -> dict:
        return {
            "id": person_id,
            "crew": [
                {"id": 101, "job": "Director"},
                {"id": 202, "job": "Producer"},
                {"id": 303, "job": "Director"},
            ],
        }


class SuperAdvancedSearchServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmdb_client = FakeTMDBClient()
        self.preference_repository = FakePreferenceRepository()
        self.user_repository = FakeUserMovieRepository()
        self.service = SuperAdvancedSearchService(
            tmdb_client=self.tmdb_client,
            preference_repository=self.preference_repository,
            user_repository=self.user_repository,
        )

    def test_default_status_filter_is_applied(self) -> None:
        result = self.service.search()

        self.assertEqual(
            result["status_filter"]["included_statuses"],
            ["new_discovery", "watch_later"],
        )
        self.assertTrue(
            result["status_filter"]["include_untracked"]
        )
        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [101, 202],
        )
        self.assertIsNone(result["results"][0]["user_data"])
        self.assertEqual(
            result["results"][1]["user_data"]["status"],
            "new_discovery",
        )

    def test_every_status_is_independently_selectable(self) -> None:
        result = self.service.search(
            included_statuses=[
                MovieStatus.WATCHED,
                MovieStatus.REWATCH,
                MovieStatus.EXCLUDED,
            ],
            include_untracked=False,
        )

        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [404, 505, 606],
        )

    def test_empty_statuses_with_untracked_returns_fresh_movies(self) -> None:
        result = self.service.search(
            included_statuses=[],
            include_untracked=True,
        )

        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [101],
        )

    def test_status_filter_runs_before_country_lookups(self) -> None:
        result = self.service.search(
            included_statuses=[MovieStatus.WATCHED],
            include_untracked=False,
        )

        self.assertEqual(
            self.tmdb_client.detail_calls,
            [404],
        )
        self.assertEqual(result["country_detail_lookups"], 1)
        self.assertEqual(result["status_match_count"], 1)

    def test_invalid_status_is_rejected_before_tmdb_call(self) -> None:
        with self.assertRaises(ValueError):
            self.service.search(
                included_statuses=["maybe"],
            )

        self.assertFalse(self.tmdb_client.discover_called)

    def test_duplicate_statuses_are_removed(self) -> None:
        result = self.service.search(
            included_statuses=[
                "rewatch",
                "rewatch",
            ],
            include_untracked=False,
        )

        self.assertEqual(
            result["status_filter"]["included_statuses"],
            ["rewatch"],
        )

    def test_exact_director_filter_is_inherited(self) -> None:
        self.preference_repository.preference["filters"][
            "include_director_ids"
        ] = [525]

        result = self.service.search()

        self.assertEqual(result["director_match_count"], 2)
        self.assertEqual(result["director_credit_lookups"], 1)
        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [101],
        )

    def test_notes_query_combines_with_default_statuses(self) -> None:
        result = self.service.search(
            notes_query="COLD ambience",
        )

        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [202],
        )
        self.assertEqual(
            result["notes_filter"]["query"],
            "COLD ambience",
        )
        self.assertEqual(self.tmdb_client.detail_calls, [202])

    def test_notes_query_can_include_a_hidden_status(self) -> None:
        result = self.service.search(
            included_statuses=[MovieStatus.WATCHED],
            include_untracked=False,
            notes_query="cold ambience",
        )

        self.assertEqual(
            [movie["id"] for movie in result["results"]],
            [404],
        )

    def test_blank_notes_query_is_rejected_before_tmdb_call(self) -> None:
        with self.assertRaises(ValueError):
            self.service.search(notes_query="   ")

        self.assertFalse(self.tmdb_client.discover_called)


if __name__ == "__main__":
    unittest.main()
