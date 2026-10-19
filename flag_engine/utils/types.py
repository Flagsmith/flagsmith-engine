import typing

import semver

from flag_engine.segments.types import ContextValue
from flag_engine.utils.semver import remove_semver_suffix


class SupportsStr(typing.Protocol):
    def __str__(self) -> str:  # pragma: no cover
        ...


def _cast_bool(value: object) -> bool:
    return value not in ("False", "false")


# Most specific first, as `bool` is a subclass of `int`.
_CASTING_FUNCTIONS: dict[type, typing.Callable[..., ContextValue]] = {
    bool: _cast_bool,
    int: int,
    float: float,
    semver.Version: remove_semver_suffix,
}


def get_casting_function(
    input_: object,
) -> typing.Callable[..., ContextValue]:
    """
    This function returns a callable to cast a value to the same type as input_
    >>> assert get_casting_function("a string") == str
    >>> assert get_casting_function(10) == int
    >>> assert get_casting_function(1.2) == float
    >>> assert get_casting_function(semver.Version.parse("3.4.5")) == remove_semver_suffix
    """
    # Exact type lookup first: this runs for every typed condition evaluated.
    if (casting_function := _CASTING_FUNCTIONS.get(type(input_))) is not None:
        return casting_function
    for type_, casting_function in _CASTING_FUNCTIONS.items():
        if isinstance(input_, type_):
            return casting_function
    return str
