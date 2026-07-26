import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.advanced_filters import AdvancedMovieFilters
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
            params={"append_to_response": "keywords"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_movie_filter_details(self, movie_id: int) -> dict:
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

    def search_people(
        self,
        query: str,
        page: int = 1,
    ) -> dict:
        cleaned_query = self._validate_search_query(query)
        self._validate_page(page)
        response = self.session.get(
            f"{BASE_URL}/search/person",
            headers=self.headers,
            params={
                "query": cleaned_query,
                "include_adult": False,
                "page": page,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def search_companies(
        self,
        query: str,
        page: int = 1,
    ) -> dict:
        cleaned_query = self._validate_search_query(query)
        self._validate_page(page)
        response = self.session.get(
            f"{BASE_URL}/search/company",
            headers=self.headers,
            params={
                "query": cleaned_query,
                "page": page,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_person_movie_credits(self, person_id: int) -> dict:
        self._validate_positive_id(person_id, "TMDB person ID")
        response = self.session.get(
            f"{BASE_URL}/person/{person_id}/movie_credits",
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def discover_movies(
        self,
        filters: AdvancedMovieFilters,
        page: int = 1,
    ) -> dict:
        self._validate_page(page)

        params = filters.to_tmdb_params()
        params["page"] = page

        response = self.session.get(
            f"{BASE_URL}/discover/movie",
            headers=self.headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _validate_search_query(query: str) -> str:
        if not isinstance(query, str):
            raise ValueError("TMDB search query must be text.")

        cleaned_query = " ".join(query.split())

        if not cleaned_query:
            raise ValueError("TMDB search query cannot be empty.")

        return cleaned_query

    @staticmethod
    def _validate_page(page: int) -> None:
        if (
            isinstance(page, bool)
            or not isinstance(page, int)
            or page < 1
        ):
            raise ValueError("TMDB page must be at least 1.")

    @staticmethod
    def _validate_positive_id(value: int, label: str) -> None:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value <= 0
        ):
            raise ValueError(f"{label} must be a positive integer.")
