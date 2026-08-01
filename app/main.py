from enum import Enum
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.advanced_filters import FilterLogic
from app.advanced_search_service import AdvancedSearchService
from app.general_entry_repository import GeneralEntryRepository
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

app = FastAPI(
    title="Movie Excluder API",
    version="1.0.0",
)

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
WEB_DIR = APP_DIR / "web"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

movie_service = MovieService()
advanced_search_service = AdvancedSearchService()
super_advanced_search_service = SuperAdvancedSearchService()
search_preference_repository = SearchPreferenceRepository()
search_state_repository = SearchStateRepository()
general_entry_repository = GeneralEntryRepository()
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

    return {
        "query": " ".join(query.split()),
        "page": response.get("page", page),
        "total_pages": response.get("total_pages", 0),
        "total_results": response.get("total_results", 0),
        "results": [
            {"id": keyword.get("id"), "name": keyword.get("name")}
            for keyword in response.get("results") or []
        ],
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
        return advanced_search_service.search(
            page=request.page,
            filters=_filter_request_to_dict(request.filters),
        )
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

        if request.filters is not None:
            search_arguments["filters"] = _filter_request_to_dict(
                request.filters
            )

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
    year: int | None = None,
    month: int | None = None,
):
    try:
        return general_entry_repository.list_entries(
            page=page,
            query=query,
            entry_type=entry_type,
            year=year,
            month=month,
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
        entry = general_entry_repository.create_entry(
            request.entry_type,
            request.title,
            request.body,
            request.url,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"message": "Entry created", "entry": entry}


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
