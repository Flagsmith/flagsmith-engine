import typing

import pytest
import semver

from flag_engine.utils.semver import remove_semver_suffix
from flag_engine.utils.types import get_casting_function


class _Int(int):
    pass


class _Float(float):
    pass


class _Str(str):
    pass


@pytest.mark.parametrize(
    "input_, segment_value, expected",
    (
        ("a string", "a string", "a string"),
        (_Str("a string"), "a string", "a string"),
        (10, "10", 10),
        (_Int(10), "10", 10),
        (1.5, "1.5", 1.5),
        (_Float(1.5), "1.5", 1.5),
        (True, "true", True),
        (True, "True", True),
        (True, "false", False),
        (True, "False", False),
        (False, "anything", True),
        (semver.Version.parse("1.2.3"), "1.2.3:semver", "1.2.3"),
    ),
)
def test_get_casting_function__casts_to_input_type(
    input_: object,
    segment_value: str,
    expected: typing.Any,
) -> None:
    # When
    result = get_casting_function(input_)(segment_value)

    # Then
    assert result == expected
    assert type(result) is type(expected)


def test_get_casting_function__semver__returns_remove_semver_suffix() -> None:
    assert get_casting_function(semver.Version.parse("1.2.3")) is remove_semver_suffix


def test_get_casting_function__unknown_type__returns_str() -> None:
    assert get_casting_function(object()) is str
