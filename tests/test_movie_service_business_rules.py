from app.database import initialize_database
from app.movie_service import MovieService


def main() -> None:
    initialize_database()

    service = MovieService()

    watched_id = 900001
    watchlist_id = 900002
    rewatch_id = 900003
    excluded_id = 900004

    watched_data = service.mark_as_watched(watched_id)

    assert watched_data["watched"] == 1
    assert watched_data["watchlist"] == 0
    assert watched_data["excluded"] == 0

    watchlist_data = service.add_to_watchlist(watchlist_id)

    assert watchlist_data["watchlist"] == 1
    assert watchlist_data["excluded"] == 0

    rewatch_data = service.mark_for_rewatch(rewatch_id)

    assert rewatch_data["rewatch"] == 1
    assert rewatch_data["watched"] == 1
    assert rewatch_data["watchlist"] == 0
    assert rewatch_data["excluded"] == 0

    service.add_to_watchlist(excluded_id)
    service.mark_for_rewatch(excluded_id)

    excluded_data = service.exclude_movie(
        excluded_id,
        notes="Not interested.",
    )

    assert excluded_data["excluded"] == 1
    assert excluded_data["watchlist"] == 0
    assert excluded_data["rewatch"] == 0
    assert excluded_data["notes"] == "Not interested."

    print("MovieService business-rule test passed.")


if __name__ == "__main__":
    main()