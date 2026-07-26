from app.advanced_filters import AdvancedMovieFilters, FilterLogic
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
        (
            directed_movie_ids,
            director_credit_lookups,
        ) = self._get_directed_movie_ids(filters)
        results = []
        country_detail_lookups = 0

        for movie in candidates:
            candidate = dict(movie)
            movie_id = candidate.get("id")

            if (
                directed_movie_ids is not None
                and (
                    not self._is_valid_tmdb_id(movie_id)
                    or movie_id not in directed_movie_ids
                )
            ):
                continue

            if filters.needs_country_details(candidate):
                if not self._is_valid_tmdb_id(movie_id):
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
            "director_credit_lookups": director_credit_lookups,
            "results": results,
        }

    def _get_directed_movie_ids(
        self,
        filters: AdvancedMovieFilters,
    ) -> tuple[set[int] | None, int]:
        if not filters.include_director_ids:
            return None, 0

        movie_id_sets = []

        for person_id in filters.include_director_ids:
            credits = self.tmdb_client.get_person_movie_credits(
                person_id
            )
            directed_movie_ids = set()

            for credit in credits.get("crew") or []:
                if (
                    str(credit.get("job") or "").casefold()
                    != "director"
                ):
                    continue

                movie_id = credit.get("id")

                if self._is_valid_tmdb_id(movie_id):
                    directed_movie_ids.add(movie_id)

            movie_id_sets.append(directed_movie_ids)

        exact_ids = set(movie_id_sets[0])

        for movie_ids in movie_id_sets[1:]:
            if filters.director_logic == FilterLogic.AND:
                exact_ids.intersection_update(movie_ids)
            else:
                exact_ids.update(movie_ids)

        return exact_ids, len(movie_id_sets)

    @staticmethod
    def _is_valid_tmdb_id(value: object) -> bool:
        return (
            isinstance(value, int)
            and not isinstance(value, bool)
            and value > 0
        )

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
