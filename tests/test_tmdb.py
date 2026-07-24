import requests

from app.tmdb_client import TMDBClient


def main() -> None:
    print("Test started")

    client = TMDBClient()
    print("TMDB client created")

    try:
        print("Requesting movie from TMDB...")

        movie = client.get_movie(603)

        print("Response received")
        print("Title:", movie["title"])
        print("Release:", movie["release_date"])

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")

    except requests.exceptions.Timeout:
        print("Timeout Error: TMDB took too long to respond.")

    except requests.exceptions.ConnectionError as err:
        print(f"Connection Error: {err}")

    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

    except Exception as err:
        print(f"Unexpected Error: {type(err).__name__}: {err}")


if __name__ == "__main__":
    main()