import uuid
from contextlib import asynccontextmanager
from enum import Enum
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Any

from pydantic import BaseModel, Field

from app.advanced_filters import FilterLogic
from app.advanced_search_service import AdvancedSearchService
from app.general_entry_repository import GeneralEntryRepository
from app.database import initialize_database, get_connection
from app.movie_service import MovieService
from app.movie_status import MovieStatus
from app.search_preference_repository import (
    SearchPreferenceRepository,
)
from app.search_state_repository import SearchStateRepository
from app.super_advanced_search_service import (
    DEFAULT_INCLUDED_STATUSES,
    SuperAdvancedSearchService,
)
from app.storage_repository import StorageRepository
from app.grey_service import GreyService


@asynccontextmanager
async def lifespan(_app: FastAPI):
    initialize_database()
    yield

app = FastAPI(
    title="Movie Excluder API",
    version="1.0.0",
    lifespan=lifespan,
)

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
WEB_DIR = APP_DIR / "web"
BANNERS_DIR = APP_DIR.parent / "data" / "banners"
BANNERS_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR = APP_DIR.parent / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
(ASSETS_DIR / "gifs_n_media").mkdir(parents=True, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)
app.mount(
    "/banners",
    StaticFiles(directory=BANNERS_DIR),
    name="banners",
)
app.mount(
    "/assets",
    StaticFiles(directory=ASSETS_DIR),
    name="assets",
)

movie_service = MovieService()
advanced_search_service = AdvancedSearchService()
super_advanced_search_service = SuperAdvancedSearchService()
search_preference_repository = SearchPreferenceRepository()
search_state_repository = SearchStateRepository()
general_entry_repository = GeneralEntryRepository()
storage_repository = StorageRepository()
grey_service = GreyService()
tmdb_lookup_client = advanced_search_service.tmdb_client


class WatchedRequest(BaseModel):
    tmdb_id: int


class CustomKeywordRequest(BaseModel):
    name: str


class MovieStatusRequest(BaseModel):
    status: str


class MovieNotesRequest(BaseModel):
    notes: str | None = None


class FavoriteRequest(BaseModel):
    is_favorite: bool


class MovieVerdictRequest(BaseModel):
    verdict: int | None = None


class GeneralEntryRequest(BaseModel):
    entry_type: str
    title: str
    body: str | None = None
    url: str | None = None
    tags: list[str] = Field(default_factory=list)
    status: str = "published"
    image_url: str | None = None


class KeywordType(str, Enum):
    ALL = "all"
    CUSTOM = "custom"
    TMDB = "tmdb"


class AdvancedFiltersRequest(BaseModel):
    include_genre_ids: list[int] = Field(default_factory=list)
    exclude_genre_ids: list[int] = Field(default_factory=list)
    genre_logic: FilterLogic = FilterLogic.OR

    include_keyword_ids: list[int] = Field(default_factory=list)
    exclude_keyword_ids: list[int] = Field(default_factory=list)
    keyword_logic: FilterLogic = FilterLogic.OR

    include_actor_ids: list[int] = Field(default_factory=list)
    actor_logic: FilterLogic = FilterLogic.OR
    include_director_ids: list[int] = Field(default_factory=list)
    director_logic: FilterLogic = FilterLogic.OR
    include_company_ids: list[int] = Field(default_factory=list)
    exclude_company_ids: list[int] = Field(default_factory=list)
    company_logic: FilterLogic = FilterLogic.OR

    include_original_languages: list[str] = Field(
        default_factory=list
    )
    exclude_original_languages: list[str] = Field(
        default_factory=list
    )
    include_origin_countries: list[str] = Field(
        default_factory=list
    )
    exclude_origin_countries: list[str] = Field(
        default_factory=list
    )
    country_logic: FilterLogic = FilterLogic.OR

    minimum_rating: float | None = None
    maximum_rating: float | None = None
    minimum_vote_count: int | None = None
    release_year_from: int | None = None
    release_year_to: int | None = None
    runtime_min: int | None = None
    runtime_max: int | None = None
    sort_by: str = "popularity.desc"
    include_adult: bool = False


class PersonalSearchFiltersRequest(BaseModel):
    included_statuses: list[MovieStatus] = Field(
        default_factory=lambda: [
            MovieStatus.NEW_DISCOVERY,
            MovieStatus.WATCH_LATER,
        ]
    )
    include_untracked: bool = True
    notes_query: str | None = None
    favorite_only: bool = False


class SearchStateRequest(BaseModel):
    mode: str = "simple"
    filters: AdvancedFiltersRequest = Field(
        default_factory=AdvancedFiltersRequest
    )
    personal_filters: PersonalSearchFiltersRequest = Field(
        default_factory=PersonalSearchFiltersRequest
    )
    selected_preference_id: int | None = None
    filters_collapsed: bool = False


class SearchPreferenceCreateRequest(BaseModel):
    name: str
    filters: AdvancedFiltersRequest = Field(
        default_factory=AdvancedFiltersRequest
    )
    is_default: bool = False
    personal_filters: PersonalSearchFiltersRequest | None = None


class SearchPreferenceUpdateRequest(BaseModel):
    name: str
    filters: AdvancedFiltersRequest
    personal_filters: PersonalSearchFiltersRequest | None = None


class AdvancedSearchExecutionRequest(BaseModel):
    filters: AdvancedFiltersRequest = Field(
        default_factory=AdvancedFiltersRequest
    )
    page: int = 1
    force_refresh: bool = False


class SuperAdvancedSearchRequest(BaseModel):
    preference_id: int | None = None
    filters: AdvancedFiltersRequest | None = None
    page: int = 1
    included_statuses: list[MovieStatus] = Field(
        default_factory=lambda: [
            MovieStatus(status)
            for status in DEFAULT_INCLUDED_STATUSES
        ]
    )
    include_untracked: bool = True
    notes_query: str | None = None
    favorite_only: bool = False
    force_refresh: bool = False


def _filter_request_to_dict(
    filters: AdvancedFiltersRequest,
) -> dict:
    if hasattr(filters, "model_dump"):
        return filters.model_dump()

    return filters.dict()


def _model_to_dict(model: BaseModel) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()

    return model.dict()


@app.get("/", include_in_schema=False)
def web_home():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/health")
def health_check():
    print("HEALTH ENDPOINT HIT", flush=True)
    return {"status": "ok"}


@app.get(
    "/images/posters/{file_path:path}",
    tags=["images"],
    summary="Serve or cache poster images locally",
)
def get_cached_poster(file_path: str):
    filename = Path(file_path).name
    if not filename or not any(
        filename.lower().endswith(ext)
        for ext in [".jpg", ".jpeg", ".png", ".webp"]
    ):
        raise HTTPException(status_code=400, detail="Invalid poster image path")

    # 1. Local disk hit
    cached_file = movie_service.poster_cache_service.get_poster_file(filename)
    if cached_file:
        return FileResponse(
            cached_file,
            media_type="image/jpeg",
            headers={"Cache-Control": "public, max-age=31536000, immutable"},
        )

    # 2. Check if movie is marked as excluded in database (invariant)
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT u.status
            FROM movies m
            JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
            WHERE m.poster_path LIKE ?
            LIMIT 1
            """,
            (f"%{filename}",),
        ).fetchone()
        if row and row["status"] == "excluded":
            raise HTTPException(
                status_code=404,
                detail="Poster caching excluded for rejected titles",
            )

    # 3. Online download and cache
    cached_file = movie_service.poster_cache_service.cache_poster(filename)
    if cached_file:
        return FileResponse(
            cached_file,
            media_type="image/jpeg",
            headers={"Cache-Control": "public, max-age=31536000, immutable"},
        )

    raise HTTPException(status_code=404, detail="Poster image unavailable offline")


@app.get("/movies/watched")
def get_watched_movies(page: int = 1):
    try:
        return movie_service.get_watched_movies_page(page)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/movies/watched")
def add_watched_movie(request: WatchedRequest):
    result = movie_service.mark_as_watched(request.tmdb_id)

    return {
        "message": "Movie marked as watched",
        "user_movie_data": result,
    }


@app.get(
    "/movies/status/{status}",
    tags=["movies"],
    summary="List movies by exact status",
)
def get_movies_by_status(status: str, page: int = 1):
    try:
        return movie_service.get_movies_by_status_page(status, page)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.get("/movies/search")
def search_movies(query: str, page: int = 1):
    print(f"Searching for: {query}", flush=True)

    try:
        result = movie_service.search_movies_page(query, page)
        print(f"Returned {len(result['results'])} results", flush=True)
        return result
    except Exception as e:
        print(f"SEARCH ERROR: {type(e).__name__}: {e}", flush=True)
        raise


@app.get(
    "/movies/library/search",
    tags=["movies"],
    summary="Search personal library across all pages or scoped to a shelf",
)
def search_personal_library(query: str = "", status: str | None = None):
    try:
        return movie_service.search_user_library(query, status)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.get(
    "/movies/library/people",
    tags=["movies"],
    summary="Search directors and actors saved in personal library",
)
def search_library_people(query: str = "", type: str | None = None, status: str | None = None):
    try:
        return movie_service.search_library_people(query=query, credit_type=type, status=status)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.get(
    "/movies/library/keywords",
    tags=["movies"],
    summary="Search keywords and personal tags saved in personal library",
)
def search_library_keywords(query: str = ""):
    try:
        results = movie_service.search_library_keywords(query=query)
        return {"results": results}
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.get(
    "/people/search",
    tags=["TMDB lookup"],
    summary="Search people for autocomplete",
)
def search_people(query: str, page: int = 1):
    try:
        response = tmdb_lookup_client.search_people(
            query,
            page=page,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "query": " ".join(query.split()),
        "page": response.get("page", page),
        "total_pages": response.get("total_pages", 0),
        "total_results": response.get("total_results", 0),
        "results": [
            {
                "id": person.get("id"),
                "name": person.get("name"),
                "known_for_department": person.get(
                    "known_for_department"
                ),
                "profile_path": person.get("profile_path"),
                "known_for_titles": [
                    item.get("title")
                    or item.get("name")
                    or item.get("original_title")
                    or item.get("original_name")
                    for item in person.get("known_for") or []
                    if (
                        item.get("title")
                        or item.get("name")
                        or item.get("original_title")
                        or item.get("original_name")
                    )
                ],
            }
            for person in response.get("results") or []
        ],
    }


@app.get(
    "/people/{person_id}",
    tags=["TMDB lookup"],
    summary="Get a person for a saved search profile",
)
def get_person(person_id: int):
    try:
        person = tmdb_lookup_client.get_person(person_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {
        "id": person.get("id"),
        "name": person.get("name"),
        "known_for_department": person.get("known_for_department"),
        "profile_path": person.get("profile_path"),
    }


@app.get(
    "/people/{person_id}/filmography",
    tags=["TMDB lookup"],
    summary="Get complete career filmography of an actor or director with local user library data",
)
def get_person_filmography(person_id: int, department: str | None = None):
    try:
        person = tmdb_lookup_client.get_person(person_id)
        credits_data = tmdb_lookup_client.get_person_movie_credits(person_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch person filmography: {error}",
        ) from error

    raw_cast = credits_data.get("cast") or []
    raw_crew = credits_data.get("crew") or []

    directing_movies_raw = [m for m in raw_crew if m.get("job") == "Director"]
    acting_movies_raw = list(raw_cast)

    all_movie_ids = list(
        {
            m["id"]
            for m in (directing_movies_raw + acting_movies_raw)
            if m.get("id")
        }
    )
    user_data_by_id = movie_service.user_repository.get_user_movie_data_bulk(
        all_movie_ids
    )

    def _normalize_movie(movie_dict, default_role=""):
        movie_id = movie_dict.get("id")
        return {
            "id": movie_id,
            "tmdb_id": movie_id,
            "title": movie_dict.get("title")
            or movie_dict.get("original_title")
            or "Untitled",
            "original_title": movie_dict.get("original_title"),
            "poster_path": movie_dict.get("poster_path"),
            "backdrop_path": movie_dict.get("backdrop_path"),
            "release_date": movie_dict.get("release_date"),
            "vote_average": movie_dict.get("vote_average"),
            "vote_count": movie_dict.get("vote_count"),
            "overview": movie_dict.get("overview"),
            "popularity": movie_dict.get("popularity", 0),
            "original_language": movie_dict.get("original_language"),
            "genre_ids": movie_dict.get("genre_ids") or [],
            "character": movie_dict.get("character"),
            "job": movie_dict.get("job", default_role),
            "credit_role": (
                movie_dict.get("character")
                or movie_dict.get("job")
                or default_role
            ),
            "user_data": user_data_by_id.get(movie_id),
        }

    directing_dict = {}
    for m in directing_movies_raw:
        mid = m.get("id")
        if mid and mid not in directing_dict:
            directing_dict[mid] = _normalize_movie(m, default_role="Director")
    directing_list = list(directing_dict.values())
    directing_list.sort(
        key=lambda m: (m.get("release_date") or ""), reverse=True
    )

    acting_dict = {}
    for m in acting_movies_raw:
        mid = m.get("id")
        if mid and mid not in acting_dict:
            acting_dict[mid] = _normalize_movie(m, default_role="Actor")
    acting_list = list(acting_dict.values())
    acting_list.sort(
        key=lambda m: (m.get("release_date") or ""), reverse=True
    )

    combined_dict = {}
    first_list = (
        directing_list
        if person.get("known_for_department") == "Directing"
        else acting_list
    )
    second_list = (
        acting_list
        if person.get("known_for_department") == "Directing"
        else directing_list
    )

    for m in first_list:
        combined_dict[m["id"]] = dict(m)
    for m in second_list:
        if m["id"] in combined_dict:
            existing = combined_dict[m["id"]]
            roles = [r for r in [existing.get("job"), m.get("character")] if r]
            if roles:
                existing["credit_role"] = ", ".join(roles)
        else:
            combined_dict[m["id"]] = dict(m)

    all_list = list(combined_dict.values())
    all_list.sort(key=lambda m: (m.get("release_date") or ""), reverse=True)

    dept_lower = (department or "").lower()
    if dept_lower == "directing":
        active_movies = directing_list
    elif dept_lower == "acting":
        active_movies = acting_list
    else:
        active_movies = all_list

    return {
        "person": {
            "id": person.get("id"),
            "name": person.get("name"),
            "known_for_department": person.get("known_for_department"),
            "profile_path": person.get("profile_path"),
            "biography": person.get("biography"),
            "birthday": person.get("birthday"),
            "place_of_birth": person.get("place_of_birth"),
        },
        "department": dept_lower or "all",
        "movies": active_movies,
        "directing_movies": directing_list,
        "acting_movies": acting_list,
        "directing_count": len(directing_list),
        "acting_count": len(acting_list),
        "total_count": len(all_list),
    }


@app.get(
    "/companies/search",
    tags=["TMDB lookup"],
    summary="Search production companies for autocomplete",
)
def search_companies(query: str, page: int = 1):
    try:
        response = tmdb_lookup_client.search_companies(
            query,
            page=page,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "query": " ".join(query.split()),
        "page": response.get("page", page),
        "total_pages": response.get("total_pages", 0),
        "total_results": response.get("total_results", 0),
        "results": [
            {
                "id": company.get("id"),
                "name": company.get("name"),
                "origin_country": company.get("origin_country"),
                "logo_path": company.get("logo_path"),
            }
            for company in response.get("results") or []
        ],
    }


@app.get(
    "/tmdb-keywords/search",
    tags=["TMDB lookup"],
    summary="Search official TMDB keywords for autocomplete",
)
def search_tmdb_keywords(query: str, page: int = 1):
    try:
        response = tmdb_lookup_client.search_keywords(query, page=page)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    raw_results = response.get("results") or []
    seen_names = set()
    deduped_results = []
    for keyword in raw_results:
        name = (keyword.get("name") or "").strip().lower()
        if name and name not in seen_names:
            seen_names.add(name)
            deduped_results.append(
                {"id": keyword.get("id"), "name": keyword.get("name")}
            )

    return {
        "query": " ".join(query.split()),
        "page": response.get("page", page),
        "total_pages": response.get("total_pages", 0),
        "total_results": len(deduped_results),
        "results": deduped_results,
    }


@app.get(
    "/tmdb-keywords/{keyword_id}",
    tags=["TMDB lookup"],
    summary="Get an official keyword for a saved search profile",
)
def get_tmdb_keyword(keyword_id: int):
    try:
        keyword = tmdb_lookup_client.get_keyword(keyword_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {"id": keyword.get("id"), "name": keyword.get("name")}


@app.get(
    "/companies/{company_id}",
    tags=["TMDB lookup"],
    summary="Get a company for a saved search profile",
)
def get_company(company_id: int):
    try:
        company = tmdb_lookup_client.get_company(company_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {
        "id": company.get("id"),
        "name": company.get("name"),
        "origin_country": company.get("origin_country"),
        "logo_path": company.get("logo_path"),
    }


@app.get(
    "/movies/notes",
    tags=["movies"],
    summary="List movies with personal notes",
)
def get_movies_with_notes(page: int = 1):
    try:
        return movie_service.get_movies_with_notes_page(page)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get(
    "/movies/notes/search",
    tags=["movies"],
    summary="Search personal movie notes",
)
def search_movie_notes(query: str):
    try:
        return movie_service.search_movie_notes(query)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.get(
    "/movies/keywords/search",
    tags=["movies"],
    summary="Search cached movies by keyword or custom tag",
)
def search_local_movies_by_keyword(
    query: str,
    keyword_type: KeywordType = KeywordType.ALL,
    page: int = 1,
):
    try:
        return movie_service.search_local_movies_by_keyword_page(
            query,
            keyword_type.value,
            page,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.get(
    "/movies/favorites",
    tags=["movies"],
    summary="List favorite movies",
)
def get_favorite_movies(page: int = 1):
    try:
        return movie_service.get_favorite_movies_page(page)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get(
    "/movies/discover/advanced",
    tags=["movies"],
    summary="Run Advanced Search",
)
def advanced_search(
    preference_id: int | None = None,
    page: int = 1,
):
    try:
        return advanced_search_service.search(
            preference_id=preference_id,
            page=page,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.post(
    "/movies/discover/advanced",
    tags=["movies"],
    summary="Run Advanced Search with direct filters",
)
def advanced_search_with_filters(
    request: AdvancedSearchExecutionRequest,
):
    try:
        search_arguments = {
            "page": request.page,
            "filters": _filter_request_to_dict(request.filters),
        }
        if request.force_refresh:
            search_arguments["force_refresh"] = True
        try:
            return advanced_search_service.search(**search_arguments)
        except TypeError:
            search_arguments.pop("force_refresh", None)
            return advanced_search_service.search(**search_arguments)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.post(
    "/movies/discover/super-advanced",
    tags=["movies"],
    summary="Run Super Advanced Search",
)
def super_advanced_search(
    request: SuperAdvancedSearchRequest,
):
    try:
        search_arguments = {
            "preference_id": request.preference_id,
            "page": request.page,
            "included_statuses": request.included_statuses,
            "include_untracked": request.include_untracked,
            "notes_query": request.notes_query,
            "favorite_only": request.favorite_only,
        }
        if request.force_refresh:
            search_arguments["force_refresh"] = True

        if request.filters is not None:
            search_arguments["filters"] = _filter_request_to_dict(
                request.filters
            )

        try:
            return super_advanced_search_service.search(
                **search_arguments,
            )
        except TypeError:
            search_arguments.pop("force_refresh", None)
            return super_advanced_search_service.search(
                **search_arguments,
            )
    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.get(
    "/movies/{tmdb_id}/related",
    tags=["movies"],
    summary="Get related movies",
)
def get_related_movies(
    tmdb_id: int,
    limit: int = 20,
    include_previously_watched: bool = False,
    include_tracked: bool | None = None,
):
    try:
        if include_tracked is not None:
            return movie_service.get_related_movies(
                tmdb_id=tmdb_id,
                limit=limit,
                include_previously_watched=include_previously_watched,
                include_tracked=include_tracked,
            )
        if include_previously_watched:
            return movie_service.get_related_movies(
                tmdb_id,
                limit,
                include_previously_watched,
            )
        return movie_service.get_related_movies(tmdb_id, limit)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get(
    "/movies/{tmdb_id}",
    tags=["movies"],
    summary="Get movie details",
)
def get_movie_details(tmdb_id: int):
    return movie_service.get_movie(tmdb_id)


@app.put(
    "/movies/{tmdb_id}/notes",
    tags=["movies"],
    summary="Set or clear personal movie notes",
)
def set_movie_notes(
    tmdb_id: int,
    request: MovieNotesRequest,
):
    try:
        user_movie_data = movie_service.set_movie_notes(
            tmdb_id,
            request.notes,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "message": "Movie notes updated",
        "user_movie_data": user_movie_data,
    }


@app.put(
    "/movies/{tmdb_id}/verdict",
    tags=["movies"],
    summary="Set or clear a personal 10-star verdict",
)
def set_movie_verdict(
    tmdb_id: int,
    request: MovieVerdictRequest,
):
    try:
        user_movie_data = movie_service.set_movie_verdict(
            tmdb_id,
            request.verdict,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {
        "message": "Movie verdict updated",
        "user_movie_data": user_movie_data,
    }


@app.put(
    "/movies/{tmdb_id}/favorite",
    tags=["movies"],
    summary="Favorite or unfavorite a movie",
)
def set_movie_favorite(
    tmdb_id: int,
    request: FavoriteRequest,
):
    try:
        user_movie_data = movie_service.set_movie_favorite(
            tmdb_id,
            request.is_favorite,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "message": (
            "Movie added to favorites"
            if request.is_favorite
            else "Movie removed from favorites"
        ),
        "user_movie_data": user_movie_data,
    }


@app.post(
    "/movies/{tmdb_id}/keywords/custom",
    tags=["movies"],
    summary="Add a custom keyword",
)
def add_custom_keyword(
    tmdb_id: int,
    request: CustomKeywordRequest,
):
    try:
        keyword = movie_service.add_custom_keyword(
            tmdb_id,
            request.name,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "message": "Custom keyword added",
        "keyword": keyword,
    }


@app.delete(
    "/movies/{tmdb_id}/keywords/custom/{keyword_id}",
    tags=["movies"],
    summary="Remove a custom keyword from one movie",
)
def remove_custom_keyword(
    tmdb_id: int,
    keyword_id: int,
):
    removed = movie_service.remove_custom_keyword(
        tmdb_id,
        keyword_id,
    )

    if not removed:
        raise HTTPException(
            status_code=404,
            detail="Custom keyword link was not found.",
        )

    return {
        "message": "Custom keyword removed from this movie"
    }


@app.delete(
    "/keywords/custom/{keyword_id}",
    tags=["movies"],
    summary="Delete a custom keyword from every movie",
)
def delete_custom_keyword(keyword_id: int):
    try:
        deleted = movie_service.delete_custom_keyword(keyword_id)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Custom keyword was not found.",
        )

    return {
        "message": "Custom keyword deleted from every movie",
        "deleted_keyword": deleted,
    }


@app.put(
    "/keywords/custom/{keyword_id}",
    tags=["movies"],
    summary="Rename or merge a custom keyword globally",
)
def rename_custom_keyword(
    keyword_id: int,
    request: CustomKeywordRequest,
):
    try:
        renamed = movie_service.rename_custom_keyword(
            keyword_id,
            request.name,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    if renamed is None:
        raise HTTPException(
            status_code=404,
            detail="Custom keyword was not found.",
        )

    message = (
        "Custom keywords merged globally"
        if renamed["action"] == "merged"
        else "Custom keyword renamed globally"
    )

    return {
        "message": message,
        "keyword": renamed,
    }


@app.put(
    "/movies/{tmdb_id}/status",
    tags=["movies"],
    summary="Set a movie status",
)
def set_movie_status(
    tmdb_id: int,
    request: MovieStatusRequest,
):
    try:
        user_movie_data = movie_service.set_movie_status(
            tmdb_id,
            request.status,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "message": "Movie status updated",
        "user_movie_data": user_movie_data,
    }


@app.delete(
    "/movies/{tmdb_id}/status",
    tags=["movies"],
    summary="Remove personal movie status (untrack)",
)
def remove_movie_status(tmdb_id: int):
    try:
        movie_service.remove_movie_status(tmdb_id)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {"message": "Movie untracked"}


@app.post(
    "/search-preferences",
    tags=["search preferences"],
    summary="Create a search preference",
    status_code=201,
)
def create_search_preference(
    request: SearchPreferenceCreateRequest,
):
    try:
        create_arguments = {"is_default": request.is_default}

        if request.personal_filters is not None:
            create_arguments["personal_filters"] = _model_to_dict(
                request.personal_filters
            )

        preference = (
            search_preference_repository.create_preference(
                request.name,
                _filter_request_to_dict(request.filters),
                **create_arguments,
            )
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "message": "Search preference created",
        "preference": preference,
    }


@app.get(
    "/search-preferences",
    tags=["search preferences"],
    summary="List search preferences",
)
def list_search_preferences():
    return search_preference_repository.list_preferences()


@app.get(
    "/search-preferences/{preference_id}",
    tags=["search preferences"],
    summary="Get a search preference",
)
def get_search_preference(preference_id: int):
    try:
        preference = search_preference_repository.get_preference(
            preference_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    if preference is None:
        raise HTTPException(
            status_code=404,
            detail="Search preference was not found.",
        )

    return preference


@app.put(
    "/search-preferences/{preference_id}",
    tags=["search preferences"],
    summary="Update a search preference",
)
def update_search_preference(
    preference_id: int,
    request: SearchPreferenceUpdateRequest,
):
    get_search_preference(preference_id)

    try:
        update_arguments = {}

        if request.personal_filters is not None:
            update_arguments["personal_filters"] = _model_to_dict(
                request.personal_filters
            )

        preference = (
            search_preference_repository.update_preference(
                preference_id,
                request.name,
                _filter_request_to_dict(request.filters),
                **update_arguments,
            )
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "message": "Search preference updated",
        "preference": preference,
    }


@app.put(
    "/search-preferences/{preference_id}/default",
    tags=["search preferences"],
    summary="Set the default search preference",
)
def set_default_search_preference(preference_id: int):
    get_search_preference(preference_id)

    try:
        preference = search_preference_repository.set_default(
            preference_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "message": "Default search preference updated",
        "preference": preference,
    }


@app.delete(
    "/search-preferences/{preference_id}",
    tags=["search preferences"],
    summary="Delete a search preference",
)
def delete_search_preference(preference_id: int):
    try:
        removed = search_preference_repository.delete_preference(
            preference_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    if not removed:
        raise HTTPException(
            status_code=404,
            detail="Search preference was not found.",
        )

    return {"message": "Search preference deleted"}


@app.get(
    "/search-state",
    tags=["search preferences"],
    summary="Get the active unsaved search state",
)
def get_search_state():
    return search_state_repository.get_state()


@app.put(
    "/search-state",
    tags=["search preferences"],
    summary="Remember the active unsaved search state",
)
def save_search_state(request: SearchStateRequest):
    try:
        return search_state_repository.save_state(
            mode=request.mode,
            filters=_filter_request_to_dict(request.filters),
            personal_filters=_model_to_dict(request.personal_filters),
            selected_preference_id=request.selected_preference_id,
            filters_collapsed=request.filters_collapsed,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get(
    "/entries",
    tags=["notes and links"],
    summary="List general notes and links",
)
def list_general_entries(
    page: int = 1,
    query: str | None = None,
    entry_type: str | None = None,
    tag: str | None = None,
    year: int | None = None,
    month: int | None = None,
    archived: bool = False,
    per_page: int = 6,
    status: str | None = "published",
    date_field: str = "created_at",
):
    try:
        repo_status = None if status == "all" else status
        return general_entry_repository.list_entries(
            page=page,
            per_page=per_page,
            query=query,
            entry_type=entry_type,
            tag=tag,
            year=year,
            month=month,
            is_archived=archived,
            status=repo_status,
            date_field=date_field,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post(
    "/entries",
    tags=["notes and links"],
    summary="Create a general note or link",
    status_code=201,
)
def create_general_entry(request: GeneralEntryRequest):
    try:
        call_kwargs = {}
        if request.image_url is not None:
            call_kwargs["image_url"] = request.image_url
        entry = general_entry_repository.create_entry(
            request.entry_type,
            request.title,
            request.body,
            request.url,
            request.tags,
            status=request.status,
            **call_kwargs,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"message": "Entry created", "entry": entry}


@app.post(
    "/entries/upload-banner",
    tags=["notes and links"],
    summary="Upload a banner image for a journal note",
)
async def upload_entry_banner(request: Request):
    content_type = request.headers.get("content-type", "").lower()
    raw_filename = request.headers.get("x-filename", "")
    contents = await request.body()
    if not contents:
        raise HTTPException(status_code=400, detail="No file selected.")
    if len(contents) > 15 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Image size exceeds the 15MB limit.",
        )
    ext = ".jpg"
    if "png" in content_type or contents.startswith(b"\x89PNG\r\n\x1a\n"):
        ext = ".png"
    elif "webp" in content_type or (contents.startswith(b"RIFF") and b"WEBP" in contents[:16]):
        ext = ".webp"
    elif "gif" in content_type or contents.startswith((b"GIF87a", b"GIF89a")):
        ext = ".gif"
    elif raw_filename:
        guessed_ext = Path(raw_filename).suffix.lower()
        if guessed_ext in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            ext = guessed_ext

    import hashlib
    file_hash = hashlib.sha256(contents).hexdigest()[:16]
    filename = f"{file_hash}{ext}"
    target_path = BANNERS_DIR / filename
    if not target_path.exists():
        with open(target_path, "wb") as f:
            f.write(contents)
    return {"url": f"/banners/{filename}"}


@app.get(
    "/entries/tags",
    tags=["notes and links"],
    summary="Get summary of all note tags with counts",
)
def get_entry_tags_summary():
    try:
        return general_entry_repository.get_tags_summary()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get(
    "/entries/timeline",
    tags=["notes and links"],
    summary="Get active years and months containing notes with counts",
)
def get_entry_timeline_summary():
    try:
        return general_entry_repository.get_timeline_summary()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.put(
    "/entries/{entry_id}/pin",
    tags=["notes and links"],
    summary="Toggle pinned state of a note",
)
def toggle_entry_pin(entry_id: int):
    try:
        entry = general_entry_repository.toggle_pin(entry_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry was not found.")
    return {"message": "Pin state updated", "entry": entry}


@app.put(
    "/entries/{entry_id}/archive",
    tags=["notes and links"],
    summary="Toggle archived state of a note",
)
def toggle_entry_archive(entry_id: int):
    try:
        entry = general_entry_repository.toggle_archive(entry_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry was not found.")
    return {"message": "Archive state updated", "entry": entry}


@app.put(
    "/entries/{entry_id}/publish",
    tags=["notes and links"],
    summary="Publish a draft note or link",
)
def publish_general_entry(entry_id: int):
    try:
        entry = general_entry_repository.publish_entry(entry_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry was not found.")
    return {"message": "Entry published", "entry": entry}


@app.get(
    "/entries/{entry_id}",
    tags=["notes and links"],
    summary="Get a single general note or link",
)
def get_general_entry(entry_id: int):
    entry = general_entry_repository.get_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry was not found.")
    return {"entry": entry}


@app.put(
    "/entries/{entry_id}",
    tags=["notes and links"],
    summary="Update a general note or link",
)
def update_general_entry(
    entry_id: int,
    request: GeneralEntryRequest,
):
    try:
        entry = general_entry_repository.update_entry(
            entry_id,
            request.entry_type,
            request.title,
            request.body,
            request.url,
            request.tags,
            status=request.status,
            image_url=request.image_url,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry was not found.")
    return {"message": "Entry updated", "entry": entry}


@app.delete(
    "/entries/{entry_id}",
    tags=["notes and links"],
    summary="Move a general note or link to trash",
)
def delete_general_entry(entry_id: int):
    try:
        removed = general_entry_repository.delete_entry(entry_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if not removed:
        raise HTTPException(status_code=404, detail="Entry was not found.")
    return {"message": "Entry moved to trash"}


@app.get(
    "/storage",
    tags=["settings"],
    summary="Show local database storage information",
)
def get_storage_summary():
    return storage_repository.get_summary()


@app.post(
    "/storage/cleanup-cache",
    tags=["settings"],
    summary="Remove old TMDB-only cached movies",
)
def cleanup_old_movie_cache(days: int = 90):
    try:
        result = storage_repository.cleanup_old_cache(days)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"message": "Old unprotected cache cleaned", **result}


@app.delete(
    "/storage/deleted-entries",
    tags=["settings"],
    summary="Permanently remove soft-deleted notes and links",
)
def purge_deleted_general_entries():
    result = storage_repository.purge_deleted_entries()
    return {"message": "Deleted entries permanently removed", **result}


class GreyChatRequest(BaseModel):
    message: str
    current_view: str = "library"
    inspected_movie_id: int | None = None
    inspected_note: dict[str, Any] | None = None
    related_movies: list[dict[str, Any]] | None = None
    active_filters: dict[str, Any] | None = None
    active_person: dict[str, Any] | None = None
    visible_movies: list[dict[str, Any]] | None = None
    notes_shelf_filter: str | None = None
    live_movie_notes: str | None = None
    history: list[dict[str, str]] | None = None
    model_mode: str = "auto"


@app.post(
    "/grey/chat",
    tags=["grey"],
    summary="Chat with Grey Cinema Companion",
)
def chat_with_grey(req: GreyChatRequest):
    return grey_service.chat(
        message=req.message,
        current_view=req.current_view,
        inspected_movie_id=req.inspected_movie_id,
        inspected_note=req.inspected_note,
        related_movies=req.related_movies,
        active_filters=req.active_filters,
        active_person=req.active_person,
        visible_movies=req.visible_movies,
        notes_shelf_filter=req.notes_shelf_filter,
        live_movie_notes=req.live_movie_notes,
        history=req.history,
        model_mode=req.model_mode,
    )



