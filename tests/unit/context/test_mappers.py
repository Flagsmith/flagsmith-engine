import typing
from decimal import Decimal

import pytest

from flag_engine.context.mappers import map_any_value_to_context_value
from flag_engine.segments.types import ContextValue

any_object = object()


@pytest.mark.parametrize(
    "value, expected_result",
    [
        (Decimal("1"), 1),
        (Decimal("1.1"), 1.1),
        ("1", 1),
        ("1.0", 1.0),
        ("-1.2", -1.2),
        ("-42", -42),
        (any_object, str(any_object)),
    ],
)
def test_map_any_value_to_context_value__returns_expected(
    value: typing.Any,
    expected_result: ContextValue,
) -> None:
    # When
    result = map_any_value_to_context_value(value)

    # Then
    assert result == expected_result
