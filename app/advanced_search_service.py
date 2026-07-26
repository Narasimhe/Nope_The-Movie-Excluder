from app.advanced_filters import AdvancedMovieFilters
from app.search_preference_repository import (
    SearchPreferenceRepository,
)
from app.tmdb_client import TMDBClient


class AdvancedSearchService:
    def __init__(
        self,
        tmdb_client: TMDBClient | None = None,
        preference_repository: SearchPreferenceRepository | None = None,
    ) -> None:
        self.tmdb_client = (
            tmdb_client
            if tmdb_client is not None
            else TMDBClient()
        )
        self.preference_repository = (
            preference_repository
            if preference_repository is not None
            else SearchPreferenceRepository()
        )

    def search(
        self,
        preference_id: int | None = None,
        page: int = 1,
    ) -> dict:
        if page < 1:
            raise ValueError("Advanced Search page must be at least 1.")

        preference = self._get_preference(preference_id)
        filters = AdvancedMovieFilters(**preference["filters"])
        tmdb_response = self.tmdb_client.discover_movies(
            filters,
            page=page,
        )
        candidates = tmdb_response.get("results") or []
        results = []
        country_detail_lookups = 0

        for movie in candidates:
            candidate = dict(movie)

            if filters.needs_country_details(candidate):
                movie_id = candidate.get("id")

                if (
                    isinstance(movie_id, bool)
                    or not isinstance(movie_id, int)
                    or movie_id <= 0
                ):
                    continue

                details = (
                    self.tmdb_client.get_movie_filter_details(
                        movie_id
                    )
                )
                country_detail_lookups += 1
                candidate["origin_country"] = (
                    details.get("origin_country") or []
                )
                candidate["production_countries"] = (
                    details.get("production_countries") or []
                )

            if filters.matches_local_rules(candidate):
                results.append(candidate)

        return {
            "preference": {
                "preference_id": preference["preference_id"],
                "name": preference["name"],
                "is_default": preference["is_default"],
            },
            "page": tmdb_response.get("page", page),
            "tmdb_total_pages": tmdb_response.get(
                "total_pages",
                0,
            ),
            "tmdb_total_results": tmdb_response.get(
                "total_results",
                0,
            ),
            "candidate_count": len(candidates),
            "result_count": len(results),
            "country_detail_lookups": country_detail_lookups,
            "results": results,
        }

    def _get_preference(
        self,
        preference_id: int | None,
    ) -> dict:
        if preference_id is None:
            preference = (
                self.preference_repository.get_default_preference()
            )

            if preference is None:
                raise LookupError(
                    "No default search preference is configured."
                )

            return preference

        preference = self.preference_repository.get_preference(
            preference_id
        )

        if preference is None:
            raise LookupError("Search preference was not found.")

        return preference
