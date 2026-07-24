from app.tmdb_client import TMDBClient


def main() -> None:
    client = TMDBClient()

    movie = client.get_movie(603)

    print("Title:", movie["title"])
    print("Release:", movie["release_date"])

    print("\nSearch results:")
    results = client.search_movies("Blade Runner")

    for item in results[:5]:
        print(
            item.get("id"),
            item.get("title"),
            item.get("release_date"),
        )


if __name__ == "__main__":
    main()