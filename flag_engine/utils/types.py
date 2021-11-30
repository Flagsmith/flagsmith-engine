import typing


def get_casting_function(input_: typing.Any) -> typing.Callable:
    """
    This function returns a callable to cast a value to the same type as input_

    eg.
        get_casting_function("a string") == str
        get_casting_function(10) == int
        get_casting_function(1.2) == float
    """

    type_ = type(input_)
    return {
        bool: lambda v: v not in ("False", "false"),
        int: int,
        float: float,
    }.get(type_, str)
