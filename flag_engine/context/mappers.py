import re
import typing
from decimal import Decimal

from flag_engine.segments.types import ContextValue, is_context_value


def map_any_value_to_context_value(value: typing.Any) -> ContextValue:
    """
    Try to coerce a value of arbitrary type to a context value type.
    Union member-specific constraints, such as max string value length, are ignored here.
    Replicate behaviour from marshmallow/pydantic V1 for number-like strings.
    For decimals return an int in case of unset exponent.
    When in doubt, return string.

    Can be used as a `pydantic.BeforeValidator`.
    """
    if is_context_value(value):
        if isinstance(value, str):
            return _map_string_value_to_context_value(value)
        return value
    if isinstance(value, Decimal):
        if value.as_tuple().exponent:
            return float(str(value))
        return int(value)
    return str(value)


_int_pattern = re.compile(r"-?[0-9]+")
_float_pattern = re.compile(r"-?[0-9]+\.[0-9]+")


def _map_string_value_to_context_value(value: str) -> ContextValue:
    if _int_pattern.fullmatch(value):
        return int(value)
    if _float_pattern.fullmatch(value):
        return float(value)
    return value
