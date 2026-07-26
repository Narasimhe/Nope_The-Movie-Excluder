from app.advanced_filters import AdvancedMovieFilters
from app.advanced_search_service import AdvancedSearchService
from app.movie_status import MovieStatus, validate_movie_status
from app.search_preference_repository import (
    SearchPreferenceRepository,
)
from app.tmdb_client import TMDBClient
from app.user_movie_repository import UserMovieRepository


DEFAULT_INCLUDED_STATUSES = (
    MovieStatus.NEW_DISCOVERY.value,
    MovieStatus.WATCH_LATER.value,
)


class SuperAdvancedSearchService(AdvancedSearchService):
    def __init__(
        self,
        tmdb_client: TMDBClient | None = None,
        preference_repository: SearchPreferenceRepository | None = None,
        user_repository: UserMovieRepository | None = None,
    ) -> None:
        super().__init__(
            tmdb_client=tmdb_client,
            preference_repository=preference_repository,
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
        included_statuses: list[str | MovieStatus] | None = None,
        include_untracked: bool = True,
        notes_query: str | None = None,
    ) -> dict:
        if page < 1:
            raise ValueError(
                "Super Advanced Search page must be at least 1."
            )

        if not isinstance(include_untracked, bool):
            raise ValueError("include_untracked must be true or false.")

        selected_statuses = self._validate_statuses(
            included_statuses
        )
        normalized_notes_query = self._normalize_notes_query(
            notes_query
        )
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
        director_matches = [
            movie
            for movie in candidates
            if (
                directed_movie_ids is None
                or (
                    self._is_valid_tmdb_id(movie.get("id"))
                    and movie["id"] in directed_movie_ids
                )
            )
        ]
        candidate_ids = [
            movie.get("id")
            for movie in director_matches
            if self._is_valid_tmdb_id(movie.get("id"))
        ]
        user_data_by_id = (
            self.user_repository.get_user_movie_data_bulk(
                candidate_ids
            )
        )
        status_matches = []

        for movie in director_matches:
            movie_id = movie.get("id")

            if not self._is_valid_tmdb_id(movie_id):
                continue

            user_data = user_data_by_id.get(movie_id)

            if user_data is None:
                if not include_untracked:
                    continue
            elif user_data.get("status") not in selected_statuses:
                continue

            if normalized_notes_query is not None:
                if user_data is None:
                    continue

                notes = str(user_data.get("notes") or "")

                if (
                    normalized_notes_query.casefold()
                    not in notes.casefold()
                ):
                    continue

            candidate = dict(movie)
            candidate["user_data"] = user_data
            status_matches.append(candidate)

        results = []
        country_detail_lookups = 0

        for candidate in status_matches:
            if filters.needs_country_details(candidate):
                details = (
                    self.tmdb_client.get_movie_filter_details(
                        candidate["id"]
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
            "status_filter": {
                "included_statuses": selected_statuses,
                "include_untracked": include_untracked,
            },
            "notes_filter": {
                "query": normalized_notes_query,
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
            "director_match_count": len(director_matches),
            "status_match_count": len(status_matches),
            "result_count": len(results),
            "country_detail_lookups": country_detail_lookups,
            "director_credit_lookups": director_credit_lookups,
            "results": results,
        }

    @staticmethod
    def _validate_statuses(
        statuses: list[str | MovieStatus] | None,
    ) -> list[str]:
        values = (
            list(DEFAULT_INCLUDED_STATUSES)
            if statuses is None
            else statuses
        )
        validated = []

        for status in values:
            value = validate_movie_status(status)

            if value not in validated:
                validated.append(value)

        return validated

    @staticmethod
    def _normalize_notes_query(
        notes_query: str | None,
    ) -> str | None:
        if notes_query is None:
            return None

        if not isinstance(notes_query, str):
            raise ValueError("notes_query must be text or null.")

        cleaned_query = " ".join(notes_query.split())

        if not cleaned_query:
            raise ValueError(
                "notes_query cannot be empty when provided."
            )

        return cleaned_query
