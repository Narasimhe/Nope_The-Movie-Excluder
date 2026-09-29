import json
import logging
import time
from typing import Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.advanced_filters import AdvancedMovieFilters
from app.config import TMDB_READ_ACCESS_TOKEN
from app.database import get_connection

logger = logging.getLogger(__name__)

BASE_URL = "https://api.themoviedb.org/3"


class TMDBClient:
    _filter_details_cache: dict[int, dict] = {}

    def __init__(self) -> None:
        if not TMDB_READ_ACCESS_TOKEN:
            raise RuntimeError("TMDB_READ_ACCESS_TOKEN is missing.")

        self.headers = {
            "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
            "accept": "application/json",
        }
        self._filter_details_cache: dict[int, dict] = {}
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        retry_strategy = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        return session

    def _cycle_session(self) -> None:
        try:
            self.session.close()
        except Exception:
            pass
        self.session = self._create_session()

    def _get_cached_country_details(self, movie_id: int) -> dict | None:
        try:
            with get_connection() as connection:
                row = connection.execute(
                    """
                    SELECT origin_country, production_countries
                    FROM movie_country_cache
                    WHERE tmdb_id = ?
                    """,
                    (movie_id,),
                ).fetchone()
                if row:
                    return {
                        "origin_country": json.loads(row["origin_country"] or "[]"),
                        "production_countries": json.loads(row["production_countries"] or "[]"),
                    }
        except Exception:
            pass
        return None

    def _save_cached_country_details(self, movie_id: int, details: dict) -> None:
        try:
            with get_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO movie_country_cache (tmdb_id, origin_country, production_countries, fetched_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(tmdb_id) DO UPDATE SET
                        origin_country = excluded.origin_country,
                        production_countries = excluded.production_countries,
                        fetched_at = CURRENT_TIMESTAMP
                    """,
                    (
                        movie_id,
                        json.dumps(details.get("origin_country") or []),
                        json.dumps(details.get("production_countries") or []),
                    ),
                )
        except Exception:
            pass

    def get_movie(self, movie_id: int) -> dict:
        for attempt in range(3):
            try:
                response = self.session.get(
                    f"{BASE_URL}/movie/{movie_id}",
                    headers=self.headers,
                    params={"append_to_response": "keywords,credits"},
                    timeout=10,
                )
                response.raise_for_status()
                return response.json()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, OSError):
                if attempt == 2:
                    raise
                self._cycle_session()
                time.sleep(0.25 * (attempt + 1))

    def get_movie_filter_details(self, movie_id: int) -> dict:
        if hasattr(getattr(self, "session", None), "last_request"):
            response = self.session.get(
                f"{BASE_URL}/movie/{movie_id}",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()

        if movie_id in self._filter_details_cache:
            return self._filter_details_cache[movie_id]

        cached = self._get_cached_country_details(movie_id)
        if cached is not None:
            self._filter_details_cache[movie_id] = cached
            return cached

        for attempt in range(3):
            try:
                response = self.session.get(
                    f"{BASE_URL}/movie/{movie_id}",
                    headers=self.headers,
                    timeout=8,
                )
                response.raise_for_status()
                data = response.json()
                filtered = {
                    "origin_country": data.get("origin_country") or [],
                    "production_countries": data.get("production_countries") or [],
                }
                self._filter_details_cache[movie_id] = filtered
                self._save_cached_country_details(movie_id, filtered)
                return filtered
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, OSError):
                self._cycle_session()
                time.sleep(0.25 * (attempt + 1))
            except requests.exceptions.HTTPError:
                break
            except Exception:
                break

        empty = {"origin_country": [], "production_countries": []}
        self._filter_details_cache[movie_id] = empty
        return empty

    def get_movie_recommendations(
        self,
        movie_id: int,
        page: int = 1,
    ) -> dict:
        self._validate_positive_id(movie_id, "TMDB movie ID")
        self._validate_page(page)
        response = self.session.get(
            f"{BASE_URL}/movie/{movie_id}/recommendations",
            headers=self.headers,
            params={"page": page},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_similar_movies(
        self,
        movie_id: int,
        page: int = 1,
    ) -> dict:
        self._validate_positive_id(movie_id, "TMDB movie ID")
        self._validate_page(page)
        response = self.session.get(
            f"{BASE_URL}/movie/{movie_id}/similar",
            headers=self.headers,
            params={"page": page},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def search_movies(self, query: str) -> list[dict]:
        return self.search_movies_page(query, page=1).get("results", [])

    def search_movies_page(self, query: str, page: int = 1) -> dict:
        cleaned_query = self._validate_search_query(query)
        self._validate_page(page)
        response = self.session.get(
            f"{BASE_URL}/search/movie",
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

    def search_keywords(
        self,
        query: str,
        page: int = 1,
    ) -> dict:
        cleaned_query = self._validate_search_query(query)
        self._validate_page(page)
        response = self.session.get(
            f"{BASE_URL}/search/keyword",
            headers=self.headers,
            params={"query": cleaned_query, "page": page},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_person(self, person_id: int) -> dict:
        self._validate_positive_id(person_id, "TMDB person ID")
        response = self.session.get(
            f"{BASE_URL}/person/{person_id}",
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_company(self, company_id: int) -> dict:
        self._validate_positive_id(company_id, "TMDB company ID")
        response = self.session.get(
            f"{BASE_URL}/company/{company_id}",
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_keyword(self, keyword_id: int) -> dict:
        self._validate_positive_id(keyword_id, "TMDB keyword ID")
        response = self.session.get(
            f"{BASE_URL}/keyword/{keyword_id}",
            headers=self.headers,
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

        for attempt in range(3):
            try:
                response = self.session.get(
                    f"{BASE_URL}/discover/movie",
                    headers=self.headers,
                    params=params,
                    timeout=10,
                )
                response.raise_for_status()
                return response.json()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, OSError):
                if attempt == 2:
                    raise
                self._cycle_session()
                time.sleep(0.25 * (attempt + 1))

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
