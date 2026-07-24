import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

        retry_strategy = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session = requests.Session()
        self.session.mount("https://", adapter)

    def get_movie(self, movie_id: int) -> dict:
        response = self.session.get(
            f"{BASE_URL}/movie/{movie_id}",
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def search_movies(self, query: str) -> list[dict]:
        response = self.session.get(
            f"{BASE_URL}/search/movie",
            headers=self.headers,
            params={"query": query},
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get("results", [])