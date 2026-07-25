from app.database import initialize_database
from app.user_movie_repository import UserMovieRepository


def main() -> None:
    initialize_database()

    repository = UserMovieRepository()

    watched_id = 910001
    excluded_id = 910002
    normal_id = 910003

    repository.set_watched(watched_id, True)
    repository.set_excluded(excluded_id, True)

    # Create a normal record that should appear in neither set.
    repository.set_watchlist(normal_id, True)

    watched_ids = repository.get_watched_movie_ids()
    excluded_ids = repository.get_excluded_movie_ids()

    assert watched_id in watched_ids
    assert excluded_id not in watched_ids
    assert normal_id not in watched_ids

    assert excluded_id in excluded_ids
    assert watched_id not in excluded_ids
    assert normal_id not in excluded_ids

    print("UserMovieRepository query-method test passed.")


if __name__ == "__main__":
    main()