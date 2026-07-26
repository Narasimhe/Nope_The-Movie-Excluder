from app.database import initialize_database
from app.movie_status import MovieStatus
from app.movie_service import MovieService


def main() -> None:
    initialize_database()

    service = MovieService()

    watched_id = 900001
    watchlist_id = 900002
    rewatch_id = 900003
    excluded_id = 900004

    watched_data = service.mark_as_watched(watched_id)

    assert watched_data["status"] == MovieStatus.WATCHED.value

    watchlist_data = service.add_to_watchlist(watchlist_id)

    assert watchlist_data["status"] == MovieStatus.WATCH_LATER.value

    rewatch_data = service.mark_for_rewatch(rewatch_id)

    assert rewatch_data["status"] == MovieStatus.REWATCH.value

    service.add_to_watchlist(excluded_id)
    service.mark_for_rewatch(excluded_id)

    excluded_data = service.exclude_movie(
        excluded_id,
        notes="Not interested.",
    )

    assert excluded_data["status"] == MovieStatus.EXCLUDED.value
    assert excluded_data["notes"] == "Not interested."

    print("MovieService business-rule test passed.")


if __name__ == "__main__":
    main()
