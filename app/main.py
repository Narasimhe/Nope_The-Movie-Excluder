from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.advanced_filters import FilterLogic
from app.advanced_search_service import AdvancedSearchService
from app.movie_service import MovieService
from app.search_preference_repository import (
    SearchPreferenceRepository,
)

app = FastAPI(
    title="Movie Excluder API",
    version="0.6.0",
)

movie_service = MovieService()
advanced_search_service = AdvancedSearchService()
search_preference_repository = SearchPreferenceRepository()


class WatchedRequest(BaseModel):
    tmdb_id: int


class CustomKeywordRequest(BaseModel):
    name: str


class MovieStatusRequest(BaseModel):
    status: str


class AdvancedFiltersRequest(BaseModel):
    include_genre_ids: list[int] = Field(default_factory=list)
    exclude_genre_ids: list[int] = Field(default_factory=list)
    genre_logic: FilterLogic = FilterLogic.OR

    include_keyword_ids: list[int] = Field(default_factory=list)
    exclude_keyword_ids: list[int] = Field(default_factory=list)
    keyword_logic: FilterLogic = FilterLogic.OR

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


@app.get(
    "/movies/{tmdb_id}",
    tags=["movies"],
    summary="Get movie details",
)
def get_movie_details(tmdb_id: int):
    return movie_service.get_movie(tmdb_id)


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
    summary="Remove a custom keyword",
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

    return {"message": "Custom keyword removed"}


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
