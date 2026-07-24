from app.database import initialize_database
from app.movie_repository import MovieRepository
from app.tmdb_client import TMDBClient


def main() -> None:
    initialize_database()

    client = TMDBClient()
    repository = MovieRepository()

    print("Fetching movie from TMDB...")
    movie = client.get_movie(603)

    print("Saving movie to SQLite...")
    repository.save_movie(movie)

    print("Reading movie from SQLite...")
    saved_movie = repository.get_movie(603)

    if saved_movie is None:
        print("Movie was not found.")
        return

    print("Title:", saved_movie["title"])
    print("TMDB ID:", saved_movie["tmdb_id"])
    print("Release date:", saved_movie["release_date"])
    print("Vote average:", saved_movie["vote_average"])


if __name__ == "__main__":
    main()