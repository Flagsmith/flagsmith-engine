import typing

import semver

from flag_engine.utils.semver import remove_semver_suffix


def get_casting_function(input_: typing.Any) -> typing.Callable:
    """
    This function returns a callable to cast a value to the same type as input_
    >>> assert get_casting_function("a string") == str
    >>> assert get_casting_function(10) == int
    >>> assert get_casting_function(1.2) == float
    >>> assert get_casting_function(semver.VersionInfo.parse("3.4.5")) == remove_semver_suffix
    """

    type_ = type(input_)
    return {
        bool: lambda v: v not in ("False", "false"),
        int: int,
        float: float,
        semver.VersionInfo: remove_semver_suffix,
    }.get(type_, str)
