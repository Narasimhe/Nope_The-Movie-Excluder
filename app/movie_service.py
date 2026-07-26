from app.movie_repository import MovieRepository
from app.tmdb_client import TMDBClient
from app.user_movie_repository import UserMovieRepository


class MovieService:
    def __init__(self) -> None:
        self.movie_repository = MovieRepository()
        self.user_repository = UserMovieRepository()
        self.tmdb_client = TMDBClient()

    def get_movie(self, tmdb_id: int) -> dict:
        local_movie = self.movie_repository.get_movie(tmdb_id)

        if local_movie is not None:
            return local_movie

        tmdb_movie = self.tmdb_client.get_movie(tmdb_id)
        self.movie_repository.save_movie(tmdb_movie)

        saved_movie = self.movie_repository.get_movie(tmdb_id)

        if saved_movie is None:
            raise RuntimeError(
                "Movie was fetched but could not be read from SQLite."
            )

        return saved_movie

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
        """
        Mark a movie as watched.

        A watched movie should no longer remain in the watchlist.
        If it was previously marked NOPE, that exclusion is removed.
        """
        self.user_repository.set_watched(tmdb_id, True)
        self.user_repository.set_watchlist(tmdb_id, False)
        self.user_repository.set_excluded(tmdb_id, False)

        return self.user_repository.get_user_movie_data(tmdb_id)

    def add_to_watchlist(self, tmdb_id: int) -> dict:
        """
        Add a movie to the watchlist.

        A NOPE movie cannot simultaneously remain in the watchlist.
        """
        self.user_repository.set_watchlist(tmdb_id, True)
        self.user_repository.set_excluded(tmdb_id, False)

        return self.user_repository.get_user_movie_data(tmdb_id)

    def mark_for_rewatch(self, tmdb_id: int) -> dict:
        """
        Mark a movie for rewatching.

        Rewatch implies that the movie has already been watched.
        """
        self.user_repository.set_rewatch(tmdb_id, True)
        self.user_repository.set_watched(tmdb_id, True)
        self.user_repository.set_watchlist(tmdb_id, False)
        self.user_repository.set_excluded(tmdb_id, False)

        return self.user_repository.get_user_movie_data(tmdb_id)

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
        """
        Mark a movie as NOPE.

        NOPE movies must not remain in the watchlist or rewatch list.
        Watched history is preserved if the movie was already watched.
        """
        self.user_repository.set_excluded(tmdb_id, True)
        self.user_repository.set_watchlist(tmdb_id, False)
        self.user_repository.set_rewatch(tmdb_id, False)

        if notes is not None:
            self.user_repository.set_notes(tmdb_id, notes.strip())

        return self.user_repository.get_user_movie_data(tmdb_id)
    
    def get_watched_movies(self) -> list[dict]:
        return self.movie_repository.get_watched_movies()  
    
    def get_watchlist_movies(self) -> list[dict]:
        return self.movie_repository.get_watchlist_movies()
    
    def get_rewatch_movies(self) -> list[dict]:
        return self.movie_repository.get_rewatch_movies()

    def get_excluded_movies(self) -> list[dict]:
        return self.movie_repository.get_excluded_movies()