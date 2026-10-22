import concurrent.futures
import logging
import time
from pathlib import Path
from typing import Any

import requests

from app.database import get_connection

logger = logging.getLogger(__name__)

POSTERS_DIR = Path(__file__).resolve().parent.parent / "data" / "posters"


class PosterCacheService:
    _offline_until: float = 0.0

    def __init__(self, cache_dir: Path | None = None):
        self.cache_dir = cache_dir or POSTERS_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    @classmethod
    def is_offline(cls) -> bool:
        return time.monotonic() < cls._offline_until

    @classmethod
    def mark_offline(cls, duration: float = 15.0) -> None:
        cls._offline_until = time.monotonic() + duration

    @classmethod
    def mark_online(cls) -> None:
        cls._offline_until = 0.0

    def get_poster_file(self, poster_path: str) -> Path | None:
        """Returns the local path if the poster is already cached on disk."""
        if not poster_path:
            return None
        filename = Path(poster_path).name
        if not filename:
            return None
        target = self.cache_dir / filename
        if target.exists() and target.is_file() and target.stat().st_size > 0:
            return target
        return None

    def cache_poster(
        self, poster_path: str, is_excluded: bool = False, timeout: float = 1.5
    ) -> Path | None:
        """
        Downloads and caches a poster image locally on disk.
        Storage invariant: NEVER caches posters for NOPE / excluded movies.
        """
        if not poster_path or is_excluded:
            return None
        filename = Path(poster_path).name
        if not filename or not any(
            filename.lower().endswith(ext)
            for ext in [".jpg", ".jpeg", ".png", ".webp"]
        ):
            return None

        target = self.cache_dir / filename
        if target.exists() and target.is_file() and target.stat().st_size > 0:
            return target

        if self.is_offline():
            return None

        url = f"https://image.tmdb.org/t/p/w500/{filename}"
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200 and resp.content:
                target.write_bytes(resp.content)
                self.mark_online()
                return target
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, OSError) as e:
            self.mark_offline(15.0)
            logger.debug(f"Could not download poster {filename} (offline circuit tripped): {e}")
        except Exception as e:
            logger.debug(f"Could not download poster {filename}: {e}")
        return None

    def cache_posters_async(self, movies: list[dict[str, Any]]) -> None:
        """Background thread caching for non-excluded movies."""
        for m in movies:
            p = m.get("poster_path")
            if not p:
                continue
            u_data = m.get("user_data")
            status = (
                u_data.get("status")
                if isinstance(u_data, dict)
                else m.get("status")
            )
            # Storage Optimization invariant: Never cache posters for NOPE movies
            if status == "excluded":
                continue
            self.executor.submit(self.cache_poster, p, False)

    def purge_excluded_poster(self, poster_path: str) -> None:
        """Storage Optimization invariant: Delete poster image for NOPE / excluded movies."""
        if not poster_path:
            return
        filename = Path(poster_path).name
        target = self.cache_dir / filename
        if target.exists() and target.is_file():
            try:
                target.unlink()
            except Exception as e:
                logger.debug(f"Could not purge excluded poster {filename}: {e}")
