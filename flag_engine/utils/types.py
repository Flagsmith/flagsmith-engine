import typing
from functools import singledispatch

import semver

from flag_engine.segments.types import ContextValue
from flag_engine.utils.semver import remove_semver_suffix


class SupportsStr(typing.Protocol):
    def __str__(self) -> str:  # pragma: no cover
        ...


@singledispatch
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
    return str


@get_casting_function.register
def _(input_: bool) -> typing.Callable[..., bool]:
    return lambda v: v not in ("False", "false")


@get_casting_function.register
def _(input_: int) -> typing.Callable[..., int]:
    return int


@get_casting_function.register
def _(input_: float) -> typing.Callable[..., float]:
    return float


@get_casting_function.register
def _(input_: semver.Version) -> typing.Callable[..., str]:
    return remove_semver_suffix
