from app.database import get_connection
from app.movie_service import MovieService


def reset_database() -> None:
    with get_connection() as connection:
        connection.execute("DELETE FROM user_movie_data")
        connection.execute("DELETE FROM movies")


def test_get_watched_movies() -> None:
    reset_database()

    service = MovieService()

    movies = [
        {
            "id": 100,
            "title": "Movie A",
            "original_title": "Movie A",
            "release_date": "2020-01-01",
            "overview": "Test movie A",
            "poster_path": None,
            "backdrop_path": None,
            "vote_average": 7.0,
        },
        {
            "id": 200,
            "title": "Movie B",
            "original_title": "Movie B",
            "release_date": "2021-01-01",
            "overview": "Test movie B",
            "poster_path": None,
            "backdrop_path": None,
            "vote_average": 7.5,
        },
        {
            "id": 300,
            "title": "Movie C",
            "original_title": "Movie C",
            "release_date": "2022-01-01",
            "overview": "Test movie C",
            "poster_path": None,
            "backdrop_path": None,
            "vote_average": 8.0,
        },
    ]

    for movie in movies:
        service.movie_repository.save_movie(movie)

    service.mark_as_watched(100)
    service.mark_as_watched(300)

    watched_movies = service.get_watched_movies()

    watched_ids = {
        movie["tmdb_id"]
        for movie in watched_movies
    }

    assert watched_ids == {100, 300}