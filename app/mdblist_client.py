import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from app.config import DEFAULT_REQUEST_TIMEOUT, MDBLIST_API_KEY
from app.database import get_connection

logger = logging.getLogger(__name__)

MDBLIST_BASE_URL = "https://mdblist.com/api/"


class MDBListClient:
    """Client for fetching third-party verified ratings via MDBList."""

    def __init__(self, api_key: str | None = None, timeout: int = DEFAULT_REQUEST_TIMEOUT) -> None:
        self.api_key = api_key or MDBLIST_API_KEY
        self.timeout = timeout

    def get_ratings(self, tmdb_id: int, force_refresh: bool = False) -> dict[str, Any] | None:
        """Retrieve ratings for a movie by TMDB ID, checking local SQLite cache first unless force_refresh is True."""
        if not force_refresh:
            cached = self._get_cached_ratings(tmdb_id)
            if cached is not None:
                return cached

        if not self.api_key:
            return self._get_cached_ratings(tmdb_id)

        live_data = self._fetch_live_ratings(tmdb_id)
        if live_data is None:
            return self._get_cached_ratings(tmdb_id)

        parsed = self._extract_ratings(live_data)
        self._cache_ratings(tmdb_id, parsed)
        return parsed

    def _get_cached_ratings(self, tmdb_id: int) -> dict[str, Any] | None:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT ratings_json
                FROM movie_ratings
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            ).fetchone()

        if row is None or not row[0]:
            return None

        try:
            return json.loads(row[0])
        except (TypeError, json.JSONDecodeError):
            return None

    def _cache_ratings(self, tmdb_id: int, ratings: dict[str, Any]) -> None:
        try:
            with get_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO movie_ratings (tmdb_id, ratings_json, fetched_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(tmdb_id) DO UPDATE SET
                        ratings_json = excluded.ratings_json,
                        fetched_at = CURRENT_TIMESTAMP
                    """,
                    (tmdb_id, json.dumps(ratings)),
                )
        except Exception as error:
            logger.warning("Failed to cache MDBList ratings for TMDB #%s: %s", tmdb_id, error)

    def _fetch_live_ratings(self, tmdb_id: int) -> dict[str, Any] | None:
        params = urllib.parse.urlencode({"apikey": self.api_key, "tm": tmdb_id})
        url = f"{MDBLIST_BASE_URL}?{params}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "MovieExcluder/1.0",
                "Accept": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                content = response.read().decode("utf-8")
                return json.loads(content)
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
            logger.warning("MDBList HTTP error for TMDB #%s: %s", tmdb_id, error)
            return None
        except Exception as error:
            logger.warning("Failed to query MDBList for TMDB #%s: %s", tmdb_id, error)
            return None

    @staticmethod
    def _extract_ratings(payload: dict[str, Any]) -> dict[str, Any]:
        ratings_list = payload.get("ratings") or []
        ratings_by_source: dict[str, dict[str, Any]] = {}
        for r in ratings_list:
            source = (r.get("source") or "").strip().lower()
            if source:
                ratings_by_source[source] = r

        tomatoes_val = ratings_by_source.get("tomatoes", {}).get("value")
        popcorn_val = ratings_by_source.get("tomatoesaudience", {}).get("value")
        imdb_item = ratings_by_source.get("imdb", {})
        letterboxd_val = ratings_by_source.get("letterboxd", {}).get("value")
        metacritic_val = ratings_by_source.get("metacritic", {}).get("value")

        return {
            "tomatoes": int(round(float(tomatoes_val))) if tomatoes_val is not None else None,
            "popcorn": int(round(float(popcorn_val))) if popcorn_val is not None else None,
            "imdb": round(float(imdb_item.get("value")), 1) if imdb_item.get("value") is not None else None,
            "imdb_votes": int(imdb_item.get("votes")) if imdb_item.get("votes") is not None else None,
            "letterboxd": round(float(letterboxd_val), 1) if letterboxd_val is not None else None,
            "metacritic": int(round(float(metacritic_val))) if metacritic_val is not None else None,
        }
