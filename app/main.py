from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.movie_service import MovieService

app = FastAPI(
    title="Movie Excluder API",
    version="0.6.0",
)

movie_service = MovieService()


class WatchedRequest(BaseModel):
    tmdb_id: int


class CustomKeywordRequest(BaseModel):
    name: str


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
