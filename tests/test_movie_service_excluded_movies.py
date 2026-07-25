from app.database import get_connection, initialize_database
from app.movie_service import MovieService


def reset_database() -> None:
    initialize_database()
    with get_connection() as connection:
        connection.execute("DELETE FROM user_movie_data")
        connection.execute("DELETE FROM movies")


def test_get_excluded_movies() -> None:
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

    service.exclude_movie(100)
    service.exclude_movie(300)

    excluded_movies = service.get_excluded_movies()

    excluded_ids = {
        movie["tmdb_id"]
        for movie in excluded_movies
    }

    assert excluded_ids == {100, 300}