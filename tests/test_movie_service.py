from app.database import initialize_database
from app.movie_service import MovieService


def main() -> None:
    initialize_database()

    service = MovieService()

    print("Searching for Blade Runner...")
    results = service.search_movies("Blade Runner")

    if not results:
        print("No results found.")
        return

    for movie in results[:5]:
        print(
            movie["tmdb_id"],
            movie["title"],
            movie["release_date"],
        )


if __name__ == "__main__":
    main()