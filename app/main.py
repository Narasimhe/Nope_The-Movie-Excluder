from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.advanced_filters import FilterLogic
from app.advanced_search_service import AdvancedSearchService
from app.movie_service import MovieService
from app.movie_status import MovieStatus
from app.search_preference_repository import (
    SearchPreferenceRepository,
)
from app.super_advanced_search_service import (
    DEFAULT_INCLUDED_STATUSES,
    SuperAdvancedSearchService,
)

app = FastAPI(
    title="Movie Excluder API",
    version="0.9.0",
)

movie_service = MovieService()
advanced_search_service = AdvancedSearchService()
super_advanced_search_service = SuperAdvancedSearchService()
search_preference_repository = SearchPreferenceRepository()
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


class SearchPreferenceCreateRequest(BaseModel):
    name: str
    filters: AdvancedFiltersRequest = Field(
        default_factory=AdvancedFiltersRequest
    )
    is_default: bool = False


class SearchPreferenceUpdateRequest(BaseModel):
    name: str
    filters: AdvancedFiltersRequest


class SuperAdvancedSearchRequest(BaseModel):
    preference_id: int | None = None
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


@app.get("/health")
def health_check():
    print("HEALTH ENDPOINT HIT", flush=True)
    return {"status": "ok"}


@app.get("/movies/watched")
def get_watched_movies():
    return movie_service.get_watched_movies()


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
def get_movies_by_status(status: str):
    try:
        return movie_service.get_movies_by_status(status)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.get("/movies/search")
def search_movies(query: str):
    print(f"Searching for: {query}", flush=True)

    try:
        result = movie_service.search_movies(query)
        print(f"Returned {len(result)} results", flush=True)
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
    "/movies/favorites",
    tags=["movies"],
    summary="List favorite movies",
)
def get_favorite_movies():
    return movie_service.get_favorite_movies()


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
    "/movies/discover/super-advanced",
    tags=["movies"],
    summary="Run Super Advanced Search",
)
def super_advanced_search(
    request: SuperAdvancedSearchRequest,
):
    try:
        return super_advanced_search_service.search(
            preference_id=request.preference_id,
            page=request.page,
            included_statuses=request.included_statuses,
            include_untracked=request.include_untracked,
            notes_query=request.notes_query,
            favorite_only=request.favorite_only,
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
        preference = (
            search_preference_repository.create_preference(
                request.name,
                _filter_request_to_dict(request.filters),
                is_default=request.is_default,
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
        preference = (
            search_preference_repository.update_preference(
                preference_id,
                request.name,
                _filter_request_to_dict(request.filters),
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
