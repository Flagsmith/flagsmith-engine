import pytest

from flag_engine.segments.utils import none


@pytest.mark.parametrize(
    "iterable, expected_result",
    (
        ([], True),
        ([False], True),
        ([False, False], True),
        ([False, True], False),
        ([True, True], False),
    ),
)
def test_segment_rule_none(
    iterable: list[bool],
    expected_result: bool,
) -> None:
    assert none(iterable) is expected_result
