from app.advanced_filters import AdvancedMovieFilters, FilterLogic
from app.search_preference_repository import (
    SearchPreferenceRepository,
)
from app.tmdb_client import TMDBClient
from app.user_movie_repository import UserMovieRepository


class AdvancedSearchService:
    MAX_EXACT_SOURCE_PAGES = 50
    PAGE_SIZE = 20

    def __init__(
        self,
        tmdb_client: TMDBClient | None = None,
        preference_repository: SearchPreferenceRepository | None = None,
        user_repository: UserMovieRepository | None = None,
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
        self.user_repository = (
            user_repository
            if user_repository is not None
            else UserMovieRepository()
        )

    def search(
        self,
        preference_id: int | None = None,
        page: int = 1,
        filters: AdvancedMovieFilters | dict | None = None,
    ) -> dict:
        if page < 1:
            raise ValueError("Advanced Search page must be at least 1.")

        preference = self._resolve_preference(
            preference_id,
            filters,
        )
        filters = AdvancedMovieFilters(**preference["filters"])
        (
            directed_movie_ids,
            director_credit_lookups,
        ) = self._get_directed_movie_ids(filters)
        (
            tmdb_response,
            candidates,
            source_pages_scanned,
            pagination_exact,
        ) = self._discover_candidates(
            filters,
            page,
            post_filtering=self._requires_post_filtering(filters),
        )
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

                try:
                    details = (
                        self.tmdb_client.get_movie_filter_details(
                            movie_id
                        )
                    )
                except Exception:
                    details = {}
                country_detail_lookups += 1
                candidate["origin_country"] = (
                    details.get("origin_country") or []
                )
                candidate["production_countries"] = (
                    details.get("production_countries") or []
                )

            if filters.matches_local_rules(candidate):
                results.append(candidate)

        filtered_total = len(results)

        filtered_pagination = (
            pagination_exact
            and self._requires_post_filtering(filters)
        )

        if filtered_pagination:
            start = (page - 1) * self.PAGE_SIZE
            page_results = results[start:start + self.PAGE_SIZE]
            visible_total_pages = max(
                1,
                (filtered_total + self.PAGE_SIZE - 1) // self.PAGE_SIZE,
            )
            visible_total_results = filtered_total
        else:
            page_results = results
            visible_total_pages = (
                tmdb_response.get("total_pages", 0)
                if pagination_exact
                else None
            )
            visible_total_results = (
                tmdb_response.get("total_results", 0)
                if pagination_exact
                else None
            )

        movie_ids = [
            movie["id"]
            for movie in page_results
            if self._is_valid_tmdb_id(movie.get("id"))
        ]
        user_data = self.user_repository.get_user_movie_data_bulk(
            movie_ids
        )
        for movie in page_results:
            movie["user_data"] = user_data.get(movie.get("id"))

        return {
            "preference": {
                "preference_id": preference["preference_id"],
                "name": preference["name"],
                "is_default": preference["is_default"],
            },
            "page": page,
            "tmdb_total_pages": visible_total_pages,
            "tmdb_total_results": visible_total_results,
            "raw_tmdb_total_pages": tmdb_response.get("total_pages", 0),
            "raw_tmdb_total_results": tmdb_response.get("total_results", 0),
            "source_pages_scanned": source_pages_scanned,
            "pagination_exact": pagination_exact,
            "has_previous_page": page > 1,
            "has_next_page": (
                page < visible_total_pages
                if pagination_exact
                else page < int(tmdb_response.get("total_pages") or 0)
            ),
            "candidate_count": len(candidates),
            "filtered_result_count": filtered_total,
            "result_count": len(page_results),
            "country_detail_lookups": country_detail_lookups,
            "director_credit_lookups": director_credit_lookups,
            "results": page_results,
        }

    def _discover_candidates(
        self,
        filters: AdvancedMovieFilters,
        page: int,
        *,
        post_filtering: bool,
    ) -> tuple[dict, list[dict], int, bool]:
        if not post_filtering:
            response = self.tmdb_client.discover_movies(filters, page=page)
            return response, response.get("results") or [], 1, True

        first_response = self.tmdb_client.discover_movies(filters, page=1)
        raw_total_pages = int(first_response.get("total_pages") or 1)

        if raw_total_pages > self.MAX_EXACT_SOURCE_PAGES:
            response = (
                first_response
                if page == 1
                else self.tmdb_client.discover_movies(filters, page=page)
            )
            return response, response.get("results") or [], 1, False

        total_pages = raw_total_pages
        candidates_by_id: dict[int, dict] = {}

        def add_candidates(response: dict) -> None:
            for movie in response.get("results") or []:
                movie_id = movie.get("id")
                if self._is_valid_tmdb_id(movie_id):
                    candidates_by_id.setdefault(movie_id, dict(movie))

        add_candidates(first_response)
        for source_page in range(2, total_pages + 1):
            add_candidates(
                self.tmdb_client.discover_movies(
                    filters,
                    page=source_page,
                )
            )

        return (
            first_response,
            list(candidates_by_id.values()),
            total_pages,
            True,
        )

    @staticmethod
    def _requires_post_filtering(
        filters: AdvancedMovieFilters,
    ) -> bool:
        return bool(
            filters.include_director_ids
            or len(filters.include_original_languages) > 1
            or filters.exclude_original_languages
            or len(filters.include_origin_countries) > 1
            or filters.exclude_origin_countries
        )

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

    def _resolve_preference(
        self,
        preference_id: int | None,
        filters: AdvancedMovieFilters | dict | None,
    ) -> dict:
        if filters is None:
            return self._get_preference(preference_id)

        if preference_id is not None:
            raise ValueError(
                "Use either a saved preference or direct filters, not both."
            )

        if isinstance(filters, AdvancedMovieFilters):
            validated_filters = filters
        elif isinstance(filters, dict):
            validated_filters = AdvancedMovieFilters(**filters)
        else:
            raise ValueError("Direct search filters must be an object.")

        return {
            "preference_id": None,
            "name": "Unsaved search",
            "is_default": False,
            "filters": validated_filters.to_dict(),
        }
