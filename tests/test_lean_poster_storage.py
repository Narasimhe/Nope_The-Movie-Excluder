import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.database import initialize_database
from app.movie_metadata_repository import MovieMetadataRepository
from app.movie_repository import MovieRepository
from app.movie_service import MovieService
from app.movie_status import MovieStatus
from app.poster_cache_service import PosterCacheService
from app.storage_repository import StorageRepository
from app.user_movie_repository import UserMovieRepository


@pytest.fixture
def test_env():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        db_path = tmp_path / "test_storage.db"
        posters_dir = tmp_path / "posters"
        posters_dir.mkdir(parents=True, exist_ok=True)

        with patch("app.database.DATABASE_PATH", db_path):
            initialize_database()

            poster_service = PosterCacheService(cache_dir=posters_dir)
            movie_repo = MovieRepository()
            user_repo = UserMovieRepository()
            metadata_repo = MovieMetadataRepository()
            storage_repo = StorageRepository()

            fake_tmdb = MagicMock()
            fake_tmdb.get_movie.return_value = {
                "id": 1891,
                "title": "The Empire Strikes Back",
                "original_title": "The Empire Strikes Back",
                "release_date": "1980-05-21",
                "overview": "Darth Vader is adamant about turning Luke.",
                "poster_path": "/starwars.jpg",
                "genres": [{"id": 878, "name": "Science Fiction"}],
                "keywords": {"keywords": [{"id": 1, "name": "space opera"}]},
                "credits": {
                    "crew": [{"id": 10, "name": "Irvin Kershner", "job": "Director"}],
                    "cast": [{"id": 20, "name": "Mark Hamill", "order": 0}],
                },
            }

            movie_service = MovieService(
                movie_repository=movie_repo,
                user_repository=user_repo,
                metadata_repository=metadata_repo,
                tmdb_client=fake_tmdb,
                poster_cache_service=poster_service,
            )

            yield {
                "db_path": db_path,
                "posters_dir": posters_dir,
                "poster_service": poster_service,
                "movie_repo": movie_repo,
                "user_repo": user_repo,
                "metadata_repo": metadata_repo,
                "storage_repo": storage_repo,
                "movie_service": movie_service,
                "fake_tmdb": fake_tmdb,
            }


def test_nope_movie_preserves_text_metadata(test_env):
    """Verifies that marking a movie as excluded (NOPE) retains credits, directors, and keywords in SQLite."""
    service: MovieService = test_env["movie_service"]

    # 1. Fetch movie initially so metadata is populated
    details = service.get_movie(1891)
    assert len(details["directors"]) == 1
    assert details["directors"][0]["name"] == "Irvin Kershner"
    assert len(details["actors"]) == 1
    assert details["actors"][0]["name"] == "Mark Hamill"
    assert len(details["keywords"]) == 1

    # 2. Mark as excluded (NOPE)
    service.set_movie_status(1891, MovieStatus.EXCLUDED)

    # 3. Verify text metadata is still preserved in SQLite
    movie_after = service.get_movie(1891)
    assert movie_after["user_data"]["status"] == "excluded"
    assert len(movie_after["directors"]) == 1
    assert movie_after["directors"][0]["name"] == "Irvin Kershner"
    assert len(movie_after["actors"]) == 1
    assert movie_after["actors"][0]["name"] == "Mark Hamill"
    assert len(movie_after["keywords"]) == 1


def test_missing_credits_auto_healing(test_env):
    """Verifies that get_movie automatically fetches and heals credits if previously purged."""
    service: MovieService = test_env["movie_service"]
    metadata_repo: MovieMetadataRepository = test_env["metadata_repo"]

    # Populate movie
    service.get_movie(1891)

    # Purge credits manually as would happen in the older broken architecture
    metadata_repo.purge_movie_metadata(1891)
    credits_empty = metadata_repo.get_movie_credits(1891)
    assert len(credits_empty.get("directors", [])) == 0
    assert len(credits_empty.get("actors", [])) == 0

    # Calling get_movie now triggers self-healing
    healed = service.get_movie(1891)
    assert len(healed["directors"]) == 1
    assert healed["directors"][0]["name"] == "Irvin Kershner"
    assert len(healed["actors"]) == 1
    assert healed["actors"][0]["name"] == "Mark Hamill"


def test_library_only_poster_caching(test_env):
    """Verifies that cache_posters_async only queues library items and skips untracked/excluded."""
    poster_service: PosterCacheService = test_env["poster_service"]
    with patch.object(poster_service, "cache_poster") as mock_cache:
        movies = [
            {"poster_path": "/untracked.jpg", "user_data": None},
            {"poster_path": "/excluded.jpg", "user_data": {"status": "excluded"}},
            {"poster_path": "/watched.jpg", "user_data": {"status": "watched"}},
            {"poster_path": "/watch_later.jpg", "user_data": {"status": "watch_later"}},
            {"poster_path": "/fav.jpg", "user_data": {"is_favorite": 1, "status": None}},
        ]
        poster_service.cache_posters_async(movies)

        # Give executor thread pool a moment to submit
        cached_paths = [call.args[0] for call in mock_cache.call_args_list]
        assert "/untracked.jpg" not in cached_paths
        assert "/excluded.jpg" not in cached_paths
        assert "/watched.jpg" in cached_paths
        assert "/watch_later.jpg" in cached_paths
        assert "/fav.jpg" in cached_paths


def test_is_library_poster_check(test_env):
    """Verifies that is_library_poster returns True only for active library titles."""
    service: MovieService = test_env["movie_service"]
    movie_repo: MovieRepository = test_env["movie_repo"]

    # Movie not in library
    assert movie_repo.is_library_poster("starwars.jpg") is False

    # Movie in library (watched)
    service.get_movie(1891)
    service.set_movie_status(1891, MovieStatus.WATCHED)
    assert movie_repo.is_library_poster("starwars.jpg") is True

    # Movie excluded -> is_library_poster is False
    service.set_movie_status(1891, MovieStatus.EXCLUDED)
    assert movie_repo.is_library_poster("starwars.jpg") is False
