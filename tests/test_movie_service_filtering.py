from app.database import initialize_database
from app.movie_service import MovieService


def main():
    initialize_database()

    service = MovieService()

    # Fake TMDB results
    movies = [
        {"id": 100, "title": "Movie A"},
        {"id": 200, "title": "Movie B"},
        {"id": 300, "title": "Movie C"},
    ]

    service.mark_as_watched(100)
    service.exclude_movie(200)

    filtered = service._filter_discovery_results(movies)

    ids = {movie["id"] for movie in filtered}

    assert 100 not in ids
    assert 200 not in ids
    assert 300 in ids

    print("MovieService filtering test passed.")


if __name__ == "__main__":
    main()