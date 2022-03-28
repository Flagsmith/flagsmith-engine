from datetime import datetime, timezone


def now_with_tz() -> datetime:
    return datetime.now(tz=timezone.utc)
