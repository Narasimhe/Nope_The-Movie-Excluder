from app.movie_metadata_repository import MovieMetadataRepository
from app.movie_repository import MovieRepository
from app.movie_status import MovieStatus, validate_movie_status
from app.tmdb_client import TMDBClient
from app.user_movie_repository import UserMovieRepository


class MovieService:
    def __init__(
        self,
        movie_repository: MovieRepository | None = None,
        user_repository: UserMovieRepository | None = None,
        metadata_repository: MovieMetadataRepository | None = None,
        tmdb_client: TMDBClient | None = None,
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

    def get_movie(self, tmdb_id: int) -> dict:
        local_movie = self.movie_repository.get_movie(tmdb_id)

        if (
            local_movie is None
            or local_movie.get("metadata_fetched_at") is None
        ):
            self._fetch_and_save_movie_metadata(tmdb_id)
            local_movie = self.movie_repository.get_movie(tmdb_id)

        if local_movie is None:
            raise RuntimeError(
                "Movie was fetched but could not be read from SQLite."
            )

        result = dict(local_movie)
        result["genres"] = self.metadata_repository.get_movie_genres(
            tmdb_id
        )
        result["keywords"] = (
            self.metadata_repository.get_movie_keywords(tmdb_id)
        )
        result["user_data"] = (
            self.user_repository.get_user_movie_data(tmdb_id)
        )
        return result

    def _fetch_and_save_movie_metadata(self, tmdb_id: int) -> None:
        tmdb_movie = self.tmdb_client.get_movie(tmdb_id)
        self.movie_repository.save_movie(tmdb_movie)

        genres = tmdb_movie.get("genres") or []
        keyword_response = tmdb_movie.get("keywords") or {}

        if isinstance(keyword_response, dict):
            keywords = keyword_response.get("keywords") or []
        else:
            keywords = []

        self.metadata_repository.replace_movie_genres(
            tmdb_id,
            genres,
        )
        self.metadata_repository.replace_tmdb_keywords(
            tmdb_id,
            keywords,
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

    def set_movie_status(
        self,
        tmdb_id: int,
        status: str | MovieStatus,
    ) -> dict:
        validated_status = validate_movie_status(status)

        if self.movie_repository.get_movie(tmdb_id) is None:
            self._fetch_and_save_movie_metadata(tmdb_id)

        return self.user_repository.set_status(
            tmdb_id,
            validated_status,
        )

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
        user_data_by_id = (
            self.user_repository.get_user_movie_data_bulk(tmdb_ids)
        )

        results = []

        for movie in movies:
            result = dict(movie)
            tmdb_id = result["tmdb_id"]
            result["genres"] = genres_by_id.get(tmdb_id, [])
            result["user_data"] = user_data_by_id.get(tmdb_id)
            results.append(result)

        return results
