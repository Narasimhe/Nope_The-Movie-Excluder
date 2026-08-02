from datetime import date, datetime
from zoneinfo import ZoneInfo


APP_TIME_ZONE_NAME = "Asia/Kolkata"
APP_TIME_ZONE = ZoneInfo(APP_TIME_ZONE_NAME)


def local_now() -> datetime:
    return datetime.now(APP_TIME_ZONE)


def local_today() -> date:
    return local_now().date()


def parse_release_date(value: str | None) -> date | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None
