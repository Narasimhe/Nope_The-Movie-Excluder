import requests

from app.config import TMDB_READ_ACCESS_TOKEN


BASE_URL = "https://api.themoviedb.org/3"


class TMDBClient:
    def __init__(self) -> None:
        if not TMDB_READ_ACCESS_TOKEN:
            raise RuntimeError("TMDB_READ_ACCESS_TOKEN is missing.")

        self.headers = {
            "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
            "accept": "application/json",
        }

    def get_movie(self, movie_id: int) -> dict:
        response = requests.get(
            f"{BASE_URL}/movie/{movie_id}",
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def search_movies(self, query: str) -> list[dict]:
        response = requests.get(
            f"{BASE_URL}/search/movie",
            headers=self.headers,
            params={"query": query},
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get("results", [])