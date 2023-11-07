from datetime import timezone

from flag_engine.utils.datetime import utcnow_with_tz


def test_utcnow_with_tz_returns_time_with_utc_timezone() -> None:
    # When
    now = utcnow_with_tz()

    # Then
    assert now.tzinfo == timezone.utc
