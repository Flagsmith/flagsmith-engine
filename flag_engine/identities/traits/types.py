import re
from decimal import Decimal

from typing import Union, Any, get_args
from typing_extensions import TypeGuard

from pydantic.types import (
    AllowInfNan,
    StringConstraints,
    StrictBool,
)
from pydantic import BeforeValidator
from typing_extensions import Annotated

from flag_engine.identities.traits.constants import TRAIT_STRING_VALUE_MAX_LENGTH

_UnconstrainedTraitValue = Union[None, int, float, bool, str]


def map_any_value_to_trait_value(value: Any) -> _UnconstrainedTraitValue:
    if _is_trait_value(value):
        if isinstance(value, str):
            return _map_string_value_to_trait_value(value)
        return value
    if isinstance(value, Decimal):
        if value.as_tuple().exponent:
            return float(str(value))
        return int(value)
    return str(value)


_int_pattern = re.compile(r"-?[0-9]+")
_float_pattern = re.compile(r"-?[0-9]+\.[0-9]+")


def _map_string_value_to_trait_value(value: str) -> _UnconstrainedTraitValue:
    if _int_pattern.fullmatch(value):
        return int(value)
    if _float_pattern.fullmatch(value):
        return float(value)
    return value


def _is_trait_value(value: Any) -> TypeGuard[_UnconstrainedTraitValue]:
    return isinstance(value, get_args(_UnconstrainedTraitValue))


TraitValue = Annotated[
    Union[
        None,
        StrictBool,
        Annotated[float, AllowInfNan(False)],
        int,
        Annotated[str, StringConstraints(max_length=TRAIT_STRING_VALUE_MAX_LENGTH)],
    ],
    BeforeValidator(map_any_value_to_trait_value),
]
