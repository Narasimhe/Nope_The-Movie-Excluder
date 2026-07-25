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

        local_results = self.movie_repository.search_movies(query)

        if local_results:
            return self._filter_discovery_results(local_results)

        tmdb_results = self.tmdb_client.search_movies(query)

        for movie in tmdb_results:
            self.movie_repository.save_movie(movie)

        results = self.movie_repository.search_movies(query)
        return self._filter_discovery_results(results)

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

        return [
            movie
            for movie in movies
            if movie["id"] not in hidden_ids
        ]

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