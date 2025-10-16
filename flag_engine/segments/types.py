from __future__ import annotations

from typing import Any, Literal, Mapping, Union, get_args

from typing_extensions import TypeGuard, TypeVar

SegmentMetadataT = TypeVar("SegmentMetadataT", default=Mapping[str, object])
FeatureMetadataT = TypeVar("FeatureMetadataT", default=Mapping[str, object])

ConditionOperator = Literal[
    "EQUAL",
    "GREATER_THAN",
    "LESS_THAN",
    "LESS_THAN_INCLUSIVE",
    "CONTAINS",
    "GREATER_THAN_INCLUSIVE",
    "NOT_CONTAINS",
    "NOT_EQUAL",
    "REGEX",
    "PERCENTAGE_SPLIT",
    "MODULO",
    "IS_SET",
    "IS_NOT_SET",
    "IN",
]

RuleType = Literal[
    "ALL",
    "ANY",
    "NONE",
]


ContextValue = Union[None, int, float, bool, str]
_context_value_types = get_args(ContextValue)


def is_context_value(value: Any) -> TypeGuard[ContextValue]:
    """
    Check if the value is a valid context value type.
    This function is used to determine if a value can be treated as a context value.
    """
    return isinstance(value, _context_value_types)
