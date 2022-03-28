from datetime import timezone

from flag_engine.utils.datetime import now_with_tz


def test_now_with_tz_returns_time_with_utc_timezone():
    # When
    now = now_with_tz()

    # Then
    assert now.tzinfo == timezone.utc
