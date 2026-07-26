from enum import Enum


class MovieStatus(str, Enum):
    NEW_DISCOVERY = "new_discovery"
    WATCH_LATER = "watch_later"
    WATCHED = "watched"
    REWATCH = "rewatch"
    EXCLUDED = "excluded"


VALID_MOVIE_STATUSES = frozenset(status.value for status in MovieStatus)


def validate_movie_status(status: str | MovieStatus) -> str:
    value = status.value if isinstance(status, MovieStatus) else status

    if value not in VALID_MOVIE_STATUSES:
        allowed = ", ".join(sorted(VALID_MOVIE_STATUSES))
        raise ValueError(
            f"Invalid movie status: {value!r}. Allowed statuses: {allowed}."
        )

    return value
