import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app import database, main
from app.database import initialize_database
from app.movie_service import MovieService
from app.poster_cache_service import PosterCacheService


@pytest.fixture
def test_env():
    PosterCacheService.mark_online()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        posters_dir = Path(temp_dir) / "posters"
        posters_dir.mkdir(parents=True, exist_ok=True)
        with patch.object(database, "DATABASE_PATH", db_path):
            initialize_database()
            poster_service = PosterCacheService(cache_dir=posters_dir)
            movie_svc = MovieService(poster_cache_service=poster_service)
            yield {
                "db_path": db_path,
                "posters_dir": posters_dir,
                "poster_service": poster_service,
                "movie_svc": movie_svc,
            }
            PosterCacheService.mark_online()


def test_poster_cache_service_caching_and_purge(test_env):
    poster_service = test_env["poster_service"]
    posters_dir = test_env["posters_dir"]

    # 1. Download & cache poster when online
    with patch("requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b"fake_jpeg_bytes"
        mock_get.return_value = mock_resp

        cached = poster_service.cache_poster("/test_poster_123.jpg")
        assert cached is not None
        assert cached.exists()
        assert cached.read_bytes() == b"fake_jpeg_bytes"

        # Subsequent hit should read from disk without calling requests.get again
        mock_get.reset_mock()
        disk_hit = poster_service.get_poster_file("/test_poster_123.jpg")
        assert disk_hit is not None
        assert disk_hit == cached
        mock_get.assert_not_called()

    # 2. Excluded / NOPE movies are never cached
    assert poster_service.cache_poster("/rejected.jpg", is_excluded=True) is None
    assert not (posters_dir / "rejected.jpg").exists()

    # 3. Purging excluded poster deletes the file from disk
    assert (posters_dir / "test_poster_123.jpg").exists()
    poster_service.purge_excluded_poster("/test_poster_123.jpg")
    assert not (posters_dir / "test_poster_123.jpg").exists()


def test_movie_service_offline_preview_fallback(test_env):
    movie_svc = test_env["movie_svc"]

    # Seed discover cache with a discovered movie
    cached_payload = {
        "page": 1,
        "results": [
            {
                "id": 99999,
                "title": "Offline Discovery",
                "release_date": "2024-05-10",
                "overview": "A film found in discover cache while offline.",
                "poster_path": "/offline_disc.jpg",
                "vote_average": 8.1,
                "vote_count": 500,
                "genre_ids": [18, 53],
            }
        ],
    }

    with database.get_connection() as conn:
        conn.execute(
            "INSERT INTO tmdb_discover_cache (cache_key, response_json) VALUES (?, ?)",
            ("test_key", json.dumps(cached_payload)),
        )

    # When offline (TMDB metadata call throws an exception):
    with patch.object(
        movie_svc,
        "_fetch_and_save_movie_metadata",
        side_effect=ConnectionError("Offline / Network unreachable"),
    ):
        result = movie_svc.get_movie(99999)

        # Should not crash, but gracefully construct local preview from discover cache
        assert result["tmdb_id"] == 99999
        assert result["title"] == "Offline Discovery"
        assert result["overview"] == "A film found in discover cache while offline."
        assert result["vote_average"] == 8.1
        assert result["is_offline_preview"] is True

        # Genres resolved from local DB
        genre_names = [g["name"] for g in result["genres"]]
        assert "Drama" in genre_names or "Genre #18" in genre_names


def test_movie_service_offline_preview_for_partially_cached_movie(test_env):
    movie_svc = test_env["movie_svc"]

    # Insert a movie into SQLite that has not had deep metadata fetched yet
    with database.get_connection() as conn:
        conn.execute(
            """
            INSERT INTO movies (tmdb_id, title, release_date, overview, vote_average, metadata_fetched_at)
            VALUES (?, ?, ?, ?, ?, NULL)
            """,
            (88888, "Cached Shelf Movie", "2023-01-01", "Already on a shelf.", 7.5),
        )

    with patch.object(
        movie_svc,
        "_fetch_and_save_movie_metadata",
        side_effect=TimeoutError("TMDB Timeout"),
    ):
        result = movie_svc.get_movie(88888)
        assert result["tmdb_id"] == 88888
        assert result["title"] == "Cached Shelf Movie"
        assert result["is_offline_preview"] is True


def test_get_cached_poster_endpoint(test_env):
    posters_dir = test_env["posters_dir"]
    poster_service = test_env["poster_service"]

    with patch("app.main.movie_service.poster_cache_service", poster_service):
        # Pre-cache a poster file
        sample_file = posters_dir / "sample_card.jpg"
        sample_file.write_bytes(b"sample_image_data")

        resp = main.get_cached_poster("sample_card.jpg")
        assert isinstance(resp, FileResponse)
        assert Path(resp.path) == sample_file
        assert "max-age=" in resp.headers.get("cache-control", "")

        # Non-existent poster while offline (requests fails)
        with patch("requests.get", side_effect=ConnectionError("Offline")):
            with pytest.raises(HTTPException) as exc:
                main.get_cached_poster("missing_offline.jpg")
            assert exc.value.status_code == 404


def test_poster_cache_service_circuit_breaker(test_env):
    poster_service = test_env["poster_service"]
    PosterCacheService.mark_online()

    with patch("requests.get", side_effect=ConnectionError("Offline")):
        # First attempt fails and trips circuit
        assert poster_service.cache_poster("/circuit_test.jpg") is None
        assert PosterCacheService.is_offline() is True

    # Next attempt should immediately return None without calling requests.get
    with patch("requests.get") as mock_get:
        assert poster_service.cache_poster("/another_poster.jpg") is None
        mock_get.assert_not_called()

    # Resetting circuit restores calls
    PosterCacheService.mark_online()
    assert PosterCacheService.is_offline() is False


def test_tmdb_client_circuit_breaker():
    from app.tmdb_client import TMDBClient
    import requests

    TMDBClient.mark_online()
    client = TMDBClient()

    with patch.object(client.session, "get", side_effect=requests.exceptions.ConnectionError("Offline")):
        with patch.object(client, "_cycle_session"):
            with pytest.raises(requests.exceptions.ConnectionError):
                client.get_movie(12345)
            assert TMDBClient.is_offline() is True

    # Immediate rejection while circuit is open (without touching session.get)
    with patch.object(client.session, "get") as mock_get:
        with pytest.raises(requests.exceptions.ConnectionError) as exc:
            client.get_movie(12345)
        assert "Offline circuit breaker active" in str(exc.value)
        mock_get.assert_not_called()

    TMDBClient.mark_online()
    assert TMDBClient.is_offline() is False


