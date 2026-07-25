from app.database import initialize_database
from app.movie_service import MovieService


class FakeMovieRepository:
    def search_movies(self, query: str) -> list[dict]:
        return [
            {"id": 100, "title": "Movie A"},
            {"id": 200, "title": "Movie B"},
            {"id": 300, "title": "Movie C"},
        ]


def main():
    initialize_database()

    service = MovieService()

    service.movie_repository = FakeMovieRepository()

    service.mark_as_watched(100)
    service.exclude_movie(200)

    results = service.search_movies("science fiction")

    ids = {movie["id"] for movie in results}

    assert 100 not in ids
    assert 200 not in ids
    assert 300 in ids

    print("MovieService search filtering test passed.")


if __name__ == "__main__":
    main()