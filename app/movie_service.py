from app.movie_repository import MovieRepository
from app.tmdb_client import TMDBClient


class MovieService:
    def __init__(self) -> None:
        self.repository = MovieRepository()
        self.tmdb_client = TMDBClient()

    def get_movie(self, tmdb_id: int) -> dict:
        local_movie = self.repository.get_movie(tmdb_id)

        if local_movie is not None:
            return local_movie

        tmdb_movie = self.tmdb_client.get_movie(tmdb_id)
        self.repository.save_movie(tmdb_movie)

        saved_movie = self.repository.get_movie(tmdb_id)

        if saved_movie is None:
            raise RuntimeError("Movie was fetched but could not be read from SQLite.")

        return saved_movie

    def search_movies(self, query: str) -> list[dict]:
        query = query.strip()

        if not query:
            return []

        local_results = self.repository.search_movies(query)

        if local_results:
            return local_results

        tmdb_results = self.tmdb_client.search_movies(query)

        for movie in tmdb_results:
            self.repository.save_movie(movie)

        return self.repository.search_movies(query)