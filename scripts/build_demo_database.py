"""Build the public, read-only-on-disk demo database template.

This script never opens or replaces ``data/movie_excluder.db``. It builds a
new temporary SQLite file, validates it, and then atomically replaces only
``data/demo.db``.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import database
from app.advanced_filters import AdvancedMovieFilters
from app.general_entry_repository import GeneralEntryRepository
from app.looking_out_for_repository import LookingOutForRepository
from app.movie_metadata_repository import MovieMetadataRepository
from app.movie_repository import MovieRepository
from app.movie_status import MovieStatus
from app.search_preference_repository import SearchPreferenceRepository
from app.user_movie_repository import UserMovieRepository


DEMO_PATH = database.DATA_DIR / "demo.db"
BUILD_PATH = database.DATA_DIR / "demo.db.building"


MOVIES = [
    {
        "id": 157336,
        "title": "Interstellar",
        "original_title": "Interstellar",
        "release_date": "2014-11-05",
        "overview": (
            "Explorers travel through a wormhole in space in an attempt to "
            "ensure humanity's survival."
        ),
        "poster_path": "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "backdrop_path": None,
        "vote_average": 8.5,
        "original_language": "en",
        "status": MovieStatus.WATCHED,
        "verdict": 9.0,
        "favorite": True,
        "notes": "A huge story that still feels intimate. Revisit the docking sequence.",
        "genres": [(12, "Adventure"), (18, "Drama"), (878, "Science Fiction")],
        "keywords": [(310, "artificial intelligence"), (9882, "space"), (10891, "giant wave")],
        "director": (525, "Christopher Nolan"),
        "actors": [(10297, "Matthew McConaughey"), (1813, "Anne Hathaway")],
        "custom_keywords": ["cosmic loneliness"],
    },
    {
        "id": 329865,
        "title": "Arrival",
        "original_title": "Arrival",
        "release_date": "2016-11-10",
        "overview": (
            "A linguist works with the military to communicate with alien lifeforms "
            "after mysterious spacecraft appear around the world."
        ),
        "poster_path": None,
        "backdrop_path": None,
        "vote_average": 7.6,
        "original_language": "en",
        "status": MovieStatus.REWATCH,
        "verdict": 8.5,
        "favorite": True,
        "notes": "Language, memory and grief folded into first contact.",
        "genres": [(18, "Drama"), (878, "Science Fiction"), (9648, "Mystery")],
        "keywords": [(9951, "alien"), (14544, "end of the world"), (208090, "linguistics")],
        "director": (137427, "Denis Villeneuve"),
        "actors": [(9273, "Amy Adams"), (17604, "Jeremy Renner")],
        "custom_keywords": ["quiet science fiction"],
    },
    {
        "id": 693134,
        "title": "Dune: Part Two",
        "original_title": "Dune: Part Two",
        "release_date": "2024-02-27",
        "overview": (
            "Paul Atreides unites with Chani and the Fremen while seeking revenge "
            "against the conspirators who destroyed his family."
        ),
        "poster_path": None,
        "backdrop_path": None,
        "vote_average": 8.1,
        "original_language": "en",
        "status": MovieStatus.WATCH_LATER,
        "verdict": None,
        "favorite": False,
        "notes": None,
        "genres": [(12, "Adventure"), (878, "Science Fiction")],
        "keywords": [(530, "prophecy"), (818, "based on novel or book"), (9672, "desert")],
        "director": (137427, "Denis Villeneuve"),
        "actors": [(1190668, "Timothée Chalamet"), (505710, "Zendaya")],
        "custom_keywords": [],
    },
    {
        "id": 603,
        "title": "The Matrix",
        "original_title": "The Matrix",
        "release_date": "1999-03-30",
        "overview": (
            "A computer hacker learns that the world he knows is a simulated reality."
        ),
        "poster_path": None,
        "backdrop_path": None,
        "vote_average": 8.2,
        "original_language": "en",
        "status": MovieStatus.EXCLUDED,
        "verdict": None,
        "favorite": False,
        "notes": "A sample Nope entry, included to demonstrate personal filtering.",
        "genres": [(28, "Action"), (878, "Science Fiction")],
        "keywords": [(2343, "magic"), (310, "artificial intelligence"), (4565, "dystopia")],
        "director": (9339, "Lana Wachowski"),
        "actors": [(6384, "Keanu Reeves"), (2975, "Laurence Fishburne")],
        "custom_keywords": [],
    },
    {
        "id": 78,
        "title": "Blade Runner",
        "original_title": "Blade Runner",
        "release_date": "1982-06-25",
        "overview": (
            "A blade runner must pursue and terminate replicants who have returned to Earth."
        ),
        "poster_path": None,
        "backdrop_path": None,
        "vote_average": 7.9,
        "original_language": "en",
        "status": MovieStatus.NEW_DISCOVERY,
        "verdict": None,
        "favorite": False,
        "notes": None,
        "genres": [(18, "Drama"), (878, "Science Fiction"), (53, "Thriller")],
        "keywords": [(310, "artificial intelligence"), (4565, "dystopia"), (9882, "space")],
        "director": (578, "Ridley Scott"),
        "actors": [(3, "Harrison Ford"), (585, "Rutger Hauer")],
        "custom_keywords": ["rainy neon"],
    },
    {
        "id": 900000001,
        "title": "A Future Story (Demo)",
        "original_title": "A Future Story (Demo)",
        "release_date": "2099-08-15",
        "overview": (
            "A clearly labelled local sample used to demonstrate the Looking Out For page."
        ),
        "poster_path": None,
        "backdrop_path": None,
        "vote_average": None,
        "original_language": "en",
        "status": None,
        "verdict": None,
        "favorite": False,
        "notes": None,
        "genres": [(878, "Science Fiction")],
        "keywords": [(9882, "space")],
        "director": (900000001, "Demo Director"),
        "actors": [(900000002, "Demo Performer")],
        "custom_keywords": ["sample upcoming release"],
    },
]


def _credits(movie: dict) -> dict:
    director_id, director_name = movie["director"]
    return {
        "crew": [{"id": director_id, "name": director_name, "job": "Director"}],
        "cast": [
            {"id": person_id, "name": name, "order": position, "character": ""}
            for position, (person_id, name) in enumerate(movie["actors"])
        ],
    }


def build_demo_database() -> Path:
    if BUILD_PATH.exists():
        BUILD_PATH.unlink()

    original_path = database.DATABASE_PATH
    database.DATABASE_PATH = BUILD_PATH
    try:
        database.initialize_database()
        movies = MovieRepository()
        users = UserMovieRepository()
        metadata = MovieMetadataRepository()

        for movie in MOVIES:
            movies.save_movie(movie)
            movies.mark_metadata_fetched(movie["id"])
            metadata.replace_movie_genres(
                movie["id"],
                [{"id": genre_id, "name": name} for genre_id, name in movie["genres"]],
            )
            metadata.replace_tmdb_keywords(
                movie["id"],
                [{"id": keyword_id, "name": name} for keyword_id, name in movie["keywords"]],
            )
            metadata.replace_movie_credits(movie["id"], _credits(movie))
            for keyword in movie["custom_keywords"]:
                metadata.add_custom_keyword(movie["id"], keyword)

            if movie["status"] is not None:
                users.set_status(movie["id"], movie["status"])
                if movie["verdict"] is not None:
                    users.set_verdict(movie["id"], movie["verdict"])
                if movie["notes"]:
                    users.set_notes(movie["id"], movie["notes"])
                if movie["favorite"]:
                    users.set_favorite(movie["id"], True)

        LookingOutForRepository().add(900000001, "2099-08-15")

        entries = GeneralEntryRepository()
        entries.create_entry(
            "note",
            "Welcome to Movie Excluder",
            (
                "This is a clean public demo database. Explore the sample statuses, "
                "favourites, verdicts and search profile, then replace them with your own.\n\n"
                "Your working database is separate from demo.db and will not be overwritten "
                "by future application updates."
            ),
            tags=["welcome", "guide", "demo"],
        )
        entries.create_entry(
            "note",
            "A sample keyword notebook",
            "- quiet science fiction\n- cosmic loneliness\n- rainy neon\n- cold ambience",
            tags=["keywords", "ideas"],
        )
        entries.create_entry(
            "link",
            "Useful movie references",
            "Official sources for movie discovery and reference.",
            "https://www.themoviedb.org/\nhttps://developer.themoviedb.org/docs",
            tags=["reference", "tmdb"],
        )

        SearchPreferenceRepository().create_preference(
            "American Sci-Fi",
            AdvancedMovieFilters(
                include_genre_ids=[878],
                include_original_languages=["en"],
                include_origin_countries=["US"],
                minimum_rating=7,
                minimum_vote_count=500,
                sort_by="vote_average.desc",
            ),
            is_default=True,
        )

        with database.get_connection() as connection:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity != "ok":
                raise RuntimeError(f"Demo database integrity check failed: {integrity}")
            connection.execute("PRAGMA optimize")
    finally:
        database.DATABASE_PATH = original_path

    BUILD_PATH.replace(DEMO_PATH)
    return DEMO_PATH


if __name__ == "__main__":
    path = build_demo_database()
    with sqlite3.connect(path) as connection:
        movie_count = connection.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
        entry_count = connection.execute(
            "SELECT COUNT(*) FROM general_entries WHERE is_deleted = 0"
        ).fetchone()[0]
    print(f"Built {path} with {movie_count} movies and {entry_count} notebook entries.")
