from app.database import initialize_database
from app.movie_repository import MovieRepository
from app.movie_status import MovieStatus
from app.user_movie_repository import UserMovieRepository


def main() -> None:
    initialize_database()

    movie_repository = MovieRepository()
    user_repository = UserMovieRepository()

    # user_movie_data has a foreign key to movies,
    # so first save a simple test movie.
    movie_repository.save_movie(
        {
            "id": 78,
            "title": "Blade Runner",
            "original_title": "Blade Runner",
            "release_date": "1982-06-25",
            "overview": "A test movie.",
            "poster_path": None,
            "backdrop_path": None,
            "vote_average": 8.0,
        }
    )

    user_repository.set_status(78, MovieStatus.REWATCH)
    user_repository.set_verdict(78, 9.0)
    user_repository.set_notes(
        78,
        "Excellent atmosphere and production design.",
    )

    result = user_repository.get_user_movie_data(78)

    print(result)

    assert result is not None
    assert result["tmdb_id"] == 78
    assert result["status"] == MovieStatus.REWATCH.value
    assert result["verdict"] == 9.0
    assert result["notes"] == (
        "Excellent atmosphere and production design."
    )

    print("UserMovieRepository test passed.")


if __name__ == "__main__":
    main()
