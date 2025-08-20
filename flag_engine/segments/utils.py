import typing

from flag_engine.segments.types import RuleType


def get_matching_function(
    segment_type: RuleType,
) -> typing.Callable[[typing.Iterable[object]], bool]:
    return {
        "ANY": any,
        "ALL": all,
        "NONE": none,
    }[segment_type]


def none(iterable: typing.Iterable[object]) -> bool:
    return not any(iterable)


def escape_double_quotes(value: str) -> str:
    """
    Escape double quotes in a string for JSONPath compatibility.
    """
    return value.replace('"', '\\"')
