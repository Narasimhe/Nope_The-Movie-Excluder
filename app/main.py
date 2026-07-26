from fastapi import FastAPI
from pydantic import BaseModel

from app.movie_service import MovieService

app = FastAPI(
    title="Movie Excluder API",
    version="0.6.0",
)

movie_service = MovieService()


class WatchedRequest(BaseModel):
    tmdb_id: int


@app.get("/health")
def health_check():
    print("HEALTH ENDPOINT HIT", flush=True)
    return {"status": "ok"}



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
