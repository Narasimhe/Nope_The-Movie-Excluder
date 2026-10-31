import json
import logging

from app.movie_metadata_repository import MovieMetadataRepository
from app.movie_repository import MovieRepository
from app.movie_status import MovieStatus, validate_movie_status
from app.poster_cache_service import PosterCacheService
from app.tmdb_client import TMDBClient
from app.user_movie_repository import UserMovieRepository

logger = logging.getLogger(__name__)


class MovieService:
    def __init__(
        self,
        movie_repository: MovieRepository | None = None,
        user_repository: UserMovieRepository | None = None,
        metadata_repository: MovieMetadataRepository | None = None,
        tmdb_client: TMDBClient | None = None,
        poster_cache_service: PosterCacheService | None = None,
    ) -> None:
        self.movie_repository = (
            movie_repository
            if movie_repository is not None
            else MovieRepository()
        )
        self.user_repository = (
            user_repository
            if user_repository is not None
            else UserMovieRepository()
        )
        self.metadata_repository = (
            metadata_repository
            if metadata_repository is not None
            else MovieMetadataRepository()
        )
        self.tmdb_client = (
            tmdb_client
            if tmdb_client is not None
            else TMDBClient()
        )
        self.poster_cache_service = (
            poster_cache_service
            if poster_cache_service is not None
            else PosterCacheService()
        )

    def is_poster_caching_allowed(self, filename: str) -> bool:
        return not self.movie_repository.is_poster_excluded(filename)

    def _find_movie_in_discover_cache(self, tmdb_id: int) -> dict | None:
        return self.movie_repository.find_in_discover_cache(tmdb_id)

    def _resolve_genre_names(self, g_ids: list[int]) -> list[dict]:
        return self.movie_repository.resolve_genre_names(g_ids)

    def get_movie(self, tmdb_id: int, force_refresh: bool = False) -> dict:
        local_movie = self.movie_repository.get_movie(tmdb_id)

        if (
            force_refresh
            or local_movie is None
            or local_movie.get("metadata_fetched_at") is None
            or int(local_movie.get("metadata_version") or 1) < 2
        ):
            try:
                self._fetch_and_save_movie_metadata(tmdb_id)
                local_movie = self.movie_repository.get_movie(tmdb_id)
            except Exception as e:
                logger.warning(
                    f"Could not fetch online metadata for movie {tmdb_id}: {e}"
                )
                if local_movie is None:
                    cached_movie = self._find_movie_in_discover_cache(tmdb_id)
                    if cached_movie:
                        self.movie_repository.save_movie(cached_movie)
                        g_ids = cached_movie.get("genre_ids") or []
                        if g_ids:
                            genre_list = self._resolve_genre_names(g_ids)
                            if genre_list:
                                self.metadata_repository.replace_movie_genres(tmdb_id, genre_list)
                        local_movie = self.movie_repository.get_movie(tmdb_id)

        if local_movie is None:
            raise RuntimeError(
                f"Movie #{tmdb_id} is not cached locally and could not be fetched while offline."
            )

        self.movie_repository.touch_movie(tmdb_id)

        result = dict(local_movie)
        result["genres"] = self.metadata_repository.get_movie_genres(
            tmdb_id
        )
        result["keywords"] = (
            self.metadata_repository.get_movie_keywords(tmdb_id)
        )
        credits = self.metadata_repository.get_movie_credits(tmdb_id)
        result["directors"] = credits.get("directors", [])
        result["actors"] = credits.get("actors", [])
        result["user_data"] = (
            self.user_repository.get_user_movie_data(tmdb_id)
        )
        result["is_offline_preview"] = bool(
            local_movie.get("metadata_fetched_at") is None
            or int(local_movie.get("metadata_version") or 1) < 2
        )
        if result.get("poster_path") and (result.get("user_data") or {}).get("status") != "excluded":
            self.poster_cache_service.cache_posters_async([result])
        return result

    def get_related_movies(
        self,
        tmdb_id: int,
        limit: int = 20,
        include_previously_watched: bool = False,
        include_tracked: bool | None = None,
    ) -> dict:
        if (
            isinstance(tmdb_id, bool)
            or not isinstance(tmdb_id, int)
            or tmdb_id <= 0
        ):
            raise ValueError("TMDB movie ID must be a positive integer.")
        if (
            isinstance(limit, bool)
            or not isinstance(limit, int)
            or limit < 1
            or limit > 20
        ):
            raise ValueError("Related movie limit must be between 1 and 20.")

        response = self.tmdb_client.get_movie_recommendations(tmdb_id)
        raw_movies = response.get("results") or []
        source = "recommendations"

        if not raw_movies:
            response = self.tmdb_client.get_similar_movies(tmdb_id)
            raw_movies = response.get("results") or []
            source = "similar"

        unique_movies = []
        seen_ids = {tmdb_id}
        for movie in raw_movies:
            movie_id = movie.get("id")
            if (
                isinstance(movie_id, int)
                and not isinstance(movie_id, bool)
                and movie_id > 0
                and movie_id not in seen_ids
            ):
                seen_ids.add(movie_id)
                unique_movies.append(movie)

        if not isinstance(include_previously_watched, bool):
            raise ValueError("include_previously_watched must be true or false.")
        if include_tracked is not None and not isinstance(include_tracked, bool):
            raise ValueError("include_tracked must be true or false.")

        formatted = self._format_tmdb_results(unique_movies)
        tracked_statuses = {
            MovieStatus.WATCHED.value,
            MovieStatus.REWATCH.value,
            MovieStatus.EXCLUDED.value,
            MovieStatus.WATCH_LATER.value,
        }
        familiar_statuses = {
            MovieStatus.WATCHED.value,
            MovieStatus.REWATCH.value,
        }

        if include_tracked is not None:
            tracked_count = sum(
                1
                for movie in formatted
                if (movie.get("user_data") or {}).get("status") in tracked_statuses
            )
            visible = (
                formatted
                if include_tracked
                else [
                    movie
                    for movie in formatted
                    if (movie.get("user_data") or {}).get("status")
                    not in tracked_statuses
                ]
            )[:limit]
            hidden_count = tracked_count
        else:
            allowed = [
                movie
                for movie in formatted
                if (movie.get("user_data") or {}).get("status")
                != MovieStatus.EXCLUDED.value
            ]
            hidden_count = sum(
                1
                for movie in allowed
                if (movie.get("user_data") or {}).get("status")
                in familiar_statuses
            )
            visible = (
                allowed
                if include_previously_watched
                else [
                    movie
                    for movie in allowed
                    if (movie.get("user_data") or {}).get("status")
                    not in familiar_statuses
                ]
            )[:limit]

        return {
            "tmdb_id": tmdb_id,
            "source": source,
            "result_count": len(visible),
            "hidden_familiar_count": hidden_count,
            "hidden_tracked_count": hidden_count,
            "include_previously_watched": include_previously_watched,
            "include_tracked": include_tracked if include_tracked is not None else include_previously_watched,
            "results": visible,
        }

    def _fetch_and_save_movie_metadata(self, tmdb_id: int) -> None:
        tmdb_movie = self.tmdb_client.get_movie(tmdb_id)
        self.movie_repository.save_movie(tmdb_movie)

        genres = tmdb_movie.get("genres") or []
        keyword_response = tmdb_movie.get("keywords") or {}

        if isinstance(keyword_response, dict):
            keywords = keyword_response.get("keywords") or []
        else:
            keywords = []

        credits = tmdb_movie.get("credits") or {}

        self.metadata_repository.replace_movie_genres(
            tmdb_id,
            genres,
        )
        self.metadata_repository.replace_tmdb_keywords(
            tmdb_id,
            keywords,
        )
        self.metadata_repository.replace_movie_credits(
            tmdb_id,
            credits if isinstance(credits, dict) else {},
        )
        self.movie_repository.mark_metadata_fetched(tmdb_id)

    def search_movies(self, query: str) -> list[dict]:
        query = query.strip()

        if not query:
            return []

        tmdb_results = self.tmdb_client.search_movies(query)

        tmdb_ids = [
            movie["id"]
            for movie in tmdb_results
            if movie.get("id") is not None
        ]

        user_data_by_id = self.user_repository.get_user_movie_data_bulk(
            tmdb_ids
        )

        results = []

        for movie in tmdb_results:
            tmdb_id = movie.get("id")

            if tmdb_id is None:
                continue

            release_date = movie.get("release_date") or ""
            release_year = release_date[:4] if release_date else None

            results.append(
                {
                    "tmdb_id": tmdb_id,
                    "title": movie.get("title"),
                    "original_title": movie.get("original_title"),
                    "release_year": release_year,
                    "release_date": release_date or None,
                    "overview": movie.get("overview"),
                    "poster_path": movie.get("poster_path"),
                    "backdrop_path": movie.get("backdrop_path"),
                    "rating": movie.get("vote_average"),
                    "vote_count": movie.get("vote_count"),
                    "genre_ids": movie.get("genre_ids", []),
                    "original_language": movie.get("original_language"),
                    "user_data": user_data_by_id.get(tmdb_id),
                }
            )

        return results

    def mark_as_watched(self, tmdb_id: int) -> dict:
        return self.set_movie_status(tmdb_id, MovieStatus.WATCHED)

    def add_to_watchlist(self, tmdb_id: int) -> dict:
        return self.set_movie_status(tmdb_id, MovieStatus.WATCH_LATER)

    def mark_for_rewatch(self, tmdb_id: int) -> dict:
        return self.set_movie_status(tmdb_id, MovieStatus.REWATCH)

    def mark_as_new_discovery(self, tmdb_id: int) -> dict:
        return self.set_movie_status(tmdb_id, MovieStatus.NEW_DISCOVERY)

    def add_custom_keyword(
        self,
        tmdb_id: int,
        name: str,
    ) -> dict:
        self.get_movie(tmdb_id)
        return self.metadata_repository.add_custom_keyword(
            tmdb_id,
            name,
        )

    def remove_custom_keyword(
        self,
        tmdb_id: int,
        keyword_id: int,
    ) -> bool:
        return self.metadata_repository.remove_custom_keyword(
            tmdb_id,
            keyword_id,
        )

    def delete_custom_keyword(
        self,
        keyword_id: int,
    ) -> dict | None:
        return self.metadata_repository.delete_custom_keyword(
            keyword_id
        )

    def rename_custom_keyword(
        self,
        keyword_id: int,
        name: str,
    ) -> dict | None:
        return self.metadata_repository.rename_custom_keyword(
            keyword_id,
            name,
        )

    def set_movie_notes(
        self,
        tmdb_id: int,
        notes: str | None,
    ) -> dict:
        if notes is not None and not isinstance(notes, str):
            raise ValueError("Movie notes must be text or null.")

        cleaned_notes = notes.strip() if notes is not None else None

        if not cleaned_notes:
            cleaned_notes = None

        if self.movie_repository.get_movie(tmdb_id) is None:
            self._fetch_and_save_movie_metadata(tmdb_id)

        self.user_repository.set_notes(tmdb_id, cleaned_notes)
        result = self.user_repository.get_user_movie_data(tmdb_id)

        if result is None:
            raise RuntimeError("Movie notes were saved but not found.")

        return result

    def set_movie_verdict(
        self,
        tmdb_id: int,
        verdict: int | None,
    ) -> dict:
        if verdict is not None and (
            isinstance(verdict, bool)
            or not isinstance(verdict, int)
            or verdict < 1
            or verdict > 10
        ):
            raise ValueError(
                "Movie verdict must be a whole number from 1 to 10, or null."
            )
        if self.movie_repository.get_movie(tmdb_id) is None:
            self._fetch_and_save_movie_metadata(tmdb_id)
        self.user_repository.set_verdict(tmdb_id, verdict)
        result = self.user_repository.get_user_movie_data(tmdb_id)
        if result is None:
            raise RuntimeError("Movie verdict was saved but not found.")
        return result

    def search_movie_notes(self, query: str) -> list[dict]:
        matching_user_data = self.user_repository.search_notes(query)
        tmdb_ids = [
            user_data["tmdb_id"]
            for user_data in matching_user_data
        ]
        movies = self.movie_repository.get_movies_by_ids(tmdb_ids)
        return self._enrich_movie_list(movies)

    def search_local_movies_by_keyword(
        self,
        query: str,
        keyword_type: str = "all",
    ) -> dict:
        search_result = (
            self.metadata_repository.search_movie_keyword_links(
                query,
                keyword_type,
            )
        )
        links = search_result["links"]
        movie_ids = list(
            dict.fromkeys(link["tmdb_id"] for link in links)
        )
        movies = self.movie_repository.get_movies_by_ids(movie_ids)
        movies.sort(
            key=lambda movie: (
                (movie.get("title") or "").casefold(),
                movie["tmdb_id"],
            )
        )
        enriched_movies = self._enrich_movie_list(movies)

        matched_keywords_by_movie: dict[int, list[dict]] = {}
        matched_keywords: dict[int, dict] = {}
        movie_ids_by_keyword: dict[int, set[int]] = {}

        for link in links:
            keyword = {
                "keyword_id": link["keyword_id"],
                "tmdb_keyword_id": link["tmdb_keyword_id"],
                "name": link["name"],
                "is_custom": link["is_custom"],
                "position": link["position"],
            }
            matched_keywords_by_movie.setdefault(
                link["tmdb_id"],
                [],
            ).append(keyword)
            matched_keywords.setdefault(
                link["keyword_id"],
                {
                    "keyword_id": link["keyword_id"],
                    "tmdb_keyword_id": link["tmdb_keyword_id"],
                    "name": link["name"],
                    "is_custom": link["is_custom"],
                },
            )
            movie_ids_by_keyword.setdefault(
                link["keyword_id"],
                set(),
            ).add(link["tmdb_id"])

        for movie in enriched_movies:
            movie["matched_keywords"] = (
                matched_keywords_by_movie.get(
                    movie["tmdb_id"],
                    [],
                )
            )

        keyword_summaries = []

        for keyword_id, keyword in matched_keywords.items():
            keyword_summaries.append(
                {
                    **keyword,
                    "movie_count": len(
                        movie_ids_by_keyword[keyword_id]
                    ),
                }
            )

        return {
            "query": search_result["query"],
            "keyword_type": search_result["keyword_type"],
            "matched_keyword_count": len(keyword_summaries),
            "movie_count": len(enriched_movies),
            "matched_keywords": keyword_summaries,
            "movies": enriched_movies,
        }

    def search_local_movies_by_keyword_page(
        self,
        query: str,
        keyword_type: str = "all",
        page: int = 1,
    ) -> dict:
        search_result = (
            self.metadata_repository.search_movie_keyword_links_page(
                query,
                keyword_type,
                page=page,
            )
        )
        movies = self.movie_repository.get_movies_by_ids(
            search_result["movie_ids"]
        )
        movies.sort(
            key=lambda movie: (
                (movie.get("title") or "").casefold(),
                movie["tmdb_id"],
            )
        )
        enriched_movies = self._enrich_movie_list(movies)
        links_by_movie: dict[int, list[dict]] = {}
        for link in search_result["links"]:
            links_by_movie.setdefault(link["tmdb_id"], []).append({
                key: link[key]
                for key in (
                    "keyword_id",
                    "tmdb_keyword_id",
                    "name",
                    "is_custom",
                    "position",
                )
            })
        for movie in enriched_movies:
            movie["matched_keywords"] = links_by_movie.get(
                movie["tmdb_id"],
                [],
            )
        return {
            "query": search_result["query"],
            "keyword_type": search_result["keyword_type"],
            "page": search_result["page"],
            "page_size": search_result["page_size"],
            "total_results": search_result["total_results"],
            "total_pages": search_result["total_pages"],
            "movies": enriched_movies,
            "results": enriched_movies,
        }

    def set_movie_favorite(
        self,
        tmdb_id: int,
        is_favorite: bool,
    ) -> dict:
        if not isinstance(is_favorite, bool):
            raise ValueError("is_favorite must be true or false.")

        return self.user_repository.set_favorite(
            tmdb_id,
            is_favorite,
        )

    def set_movie_status(
        self,
        tmdb_id: int,
        status: str | MovieStatus,
    ) -> dict:
        validated_status = validate_movie_status(status)

        local_movie = self.movie_repository.get_movie(tmdb_id)
        if local_movie is None:
            try:
                self._fetch_and_save_movie_metadata(tmdb_id)
                local_movie = self.movie_repository.get_movie(tmdb_id)
            except Exception:
                cached_movie = self._find_movie_in_discover_cache(tmdb_id)
                if cached_movie:
                    self.movie_repository.save_movie(cached_movie)
                    local_movie = self.movie_repository.get_movie(tmdb_id)

        res = self.user_repository.set_status(
            tmdb_id,
            validated_status,
        )

        # Storage optimization invariant: NOPE movies never cache posters or bloated metadata
        if validated_status == MovieStatus.EXCLUDED:
            if local_movie and local_movie.get("poster_path"):
                self.poster_cache_service.purge_excluded_poster(local_movie["poster_path"])
            self.metadata_repository.purge_movie_metadata(tmdb_id)
        elif local_movie and local_movie.get("poster_path"):
            self.poster_cache_service.cache_posters_async([local_movie])

        return res

    def remove_movie_status(self, tmdb_id: int) -> None:
        if (
            isinstance(tmdb_id, bool)
            or not isinstance(tmdb_id, int)
            or tmdb_id <= 0
        ):
            raise ValueError("TMDB movie ID must be a positive integer.")
        self.user_repository.remove_status(tmdb_id)

    def _filter_discovery_results(self, movies: list[dict]) -> list[dict]:
        watched_ids = self.user_repository.get_watched_movie_ids()
        excluded_ids = self.user_repository.get_excluded_movie_ids()

        hidden_ids = watched_ids | excluded_ids

        filtered_movies = []

        for movie in movies:
            movie_id = movie.get("tmdb_id", movie.get("id"))

            if movie_id is not None and movie_id not in hidden_ids:
                filtered_movies.append(movie)

        return filtered_movies  

    def exclude_movie(self, tmdb_id: int, notes: str | None = None) -> dict:
        self.set_movie_status(tmdb_id, MovieStatus.EXCLUDED)

        if notes is not None:
            self.user_repository.set_notes(tmdb_id, notes.strip())

        return self.user_repository.get_user_movie_data(tmdb_id)
    
    def get_watched_movies(self) -> list[dict]:
        return self._enrich_movie_list(
            self.movie_repository.get_watched_movies()
        )
    
    def get_watchlist_movies(self) -> list[dict]:
        return self._enrich_movie_list(
            self.movie_repository.get_watchlist_movies()
        )
    
    def get_rewatch_movies(self) -> list[dict]:
        return self._enrich_movie_list(
            self.movie_repository.get_rewatch_movies()
        )

    def get_excluded_movies(self) -> list[dict]:
        return self._enrich_movie_list(
            self.movie_repository.get_excluded_movies()
        )

    def get_favorite_movies(self) -> list[dict]:
        return self._enrich_movie_list(
            self.movie_repository.get_favorite_movies()
        )

    def get_new_discovery_movies(self) -> list[dict]:
        return self._enrich_movie_list(
            self.movie_repository.get_new_discovery_movies()
        )

    def get_movies_by_status(
        self,
        status: str | MovieStatus,
    ) -> list[dict]:
        validated_status = validate_movie_status(status)
        return self._enrich_movie_list(
            self.movie_repository.get_movies_by_status(
                validated_status
            )
        )

    def get_movies_by_status_page(
        self,
        status: str | MovieStatus,
        page: int = 1,
    ) -> dict:
        return self._enrich_page(
            self.movie_repository.get_movies_by_status_page(status, page)
        )

    def get_watched_movies_page(self, page: int = 1) -> dict:
        return self._enrich_page(
            self.movie_repository.get_watched_movies_page(page)
        )

    def get_favorite_movies_page(self, page: int = 1) -> dict:
        return self._enrich_page(
            self.movie_repository.get_favorite_movies_page(page)
        )

    def get_movies_with_notes_page(self, page: int = 1) -> dict:
        return self._enrich_page(
            self.movie_repository.get_movies_with_notes_page(page)
        )

    def _enrich_page(self, page_data: dict) -> dict:
        result = dict(page_data)
        result["results"] = self._enrich_movie_list(
            page_data["results"]
        )
        return result

    @staticmethod
    def _empty_page(page: int = 1, page_size: int = 20) -> dict:
        return {
            "page": page,
            "page_size": page_size,
            "total_results": 0,
            "total_pages": 1,
            "results": [],
        }

    def _enrich_movie_list(
        self,
        movies: list[dict],
    ) -> list[dict]:
        tmdb_ids = [
            movie["tmdb_id"]
            for movie in movies
        ]
        genres_by_id = (
            self.metadata_repository.get_movie_genres_bulk(tmdb_ids)
        )
        credits_by_id = (
            self.metadata_repository.get_movie_credits_bulk(tmdb_ids)
        )
        keywords_by_id = (
            self.metadata_repository.get_movie_keywords_bulk(tmdb_ids)
        )
        user_data_by_id = (
            self.user_repository.get_user_movie_data_bulk(tmdb_ids)
        )

        results = []

        for movie in movies:
            result = dict(movie)
            tmdb_id = result["tmdb_id"]
            movie_genres = genres_by_id.get(tmdb_id, [])
            result["genres"] = [
                {**g, "id": g.get("tmdb_genre_id", g.get("id"))}
                for g in movie_genres
            ]
            movie_credits = credits_by_id.get(tmdb_id, {})
            result["directors"] = movie_credits.get("directors", [])
            result["actors"] = movie_credits.get("actors", [])
            result["keywords"] = keywords_by_id.get(tmdb_id, [])
            result["user_data"] = user_data_by_id.get(tmdb_id)
            results.append(result)

        self.poster_cache_service.cache_posters_async(results)
        return results

    def search_user_library(
        self,
        query: str = "",
        status: str | None = None,
    ) -> list[dict]:
        movies = self.movie_repository.search_user_library(query, status)
        return self._enrich_movie_list(movies)

    def search_library_people(
        self,
        query: str,
        credit_type: str | None = None,
        status: str | None = None,
    ) -> list[dict]:
        return self.metadata_repository.search_library_people(
            query=query,
            credit_type=credit_type,
            status=status,
        )

    def search_library_keywords(
        self,
        query: str,
    ) -> list[dict]:
        return self.metadata_repository.search_library_keywords(
            query=query,
        )

    def search_movies_page(self, query: str, page: int = 1) -> dict:
        query = query.strip()
        if not query:
            return self._empty_page(page)
        response = self.tmdb_client.search_movies_page(query, page=page)
        results = self._format_tmdb_results(response.get("results") or [])
        total_pages = min(int(response.get("total_pages") or 0), 500)
        return {
            "page": int(response.get("page") or page),
            "page_size": 20,
            "total_results": int(response.get("total_results") or 0),
            "total_pages": max(1, total_pages),
            "results": results,
        }

    def _format_tmdb_results(self, tmdb_results: list[dict]) -> list[dict]:
        tmdb_ids = [
            movie["id"] for movie in tmdb_results
            if movie.get("id") is not None
        ]
        user_data_by_id = self.user_repository.get_user_movie_data_bulk(
            tmdb_ids
        )
        results = []
        for movie in tmdb_results:
            tmdb_id = movie.get("id")
            if tmdb_id is None:
                continue
            release_date = movie.get("release_date") or ""
            results.append({
                "tmdb_id": tmdb_id,
                "title": movie.get("title"),
                "original_title": movie.get("original_title"),
                "release_year": release_date[:4] or None,
                "release_date": release_date or None,
                "overview": movie.get("overview"),
                "poster_path": movie.get("poster_path"),
                "backdrop_path": movie.get("backdrop_path"),
                "rating": movie.get("vote_average"),
                "vote_count": movie.get("vote_count"),
                "genre_ids": movie.get("genre_ids", []),
                "original_language": movie.get("original_language"),
                "user_data": user_data_by_id.get(tmdb_id),
            })
        return results
