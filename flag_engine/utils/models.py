import enum
import typing
from dataclasses import dataclass


class FlagsmithValueType(enum.Enum):
    STRING = "str"
    INTEGER = "int"
    BOOLEAN = "bool"
    FLOAT = "float"
    NONE = "nonetype"


@dataclass
class FlagsmithValue:
    value: str
    value_type: FlagsmithValueType = FlagsmithValueType.STRING

    @classmethod
    def from_untyped_value(cls, untyped_value: typing.Any) -> "FlagsmithValue":
        try:
            type_ = type(untyped_value).__name__.lower()
            flagsmith_value_type = FlagsmithValueType(type_)
        except ValueError:
            flagsmith_value_type = FlagsmithValueType.STRING

        return cls(value=str(untyped_value), value_type=flagsmith_value_type)

    @property
    def casting_function(self) -> typing.Callable[[typing.Any], typing.Any]:
        return {
            FlagsmithValueType.BOOLEAN: lambda v: v not in ("False", "false"),
            FlagsmithValueType.INTEGER: int,
            FlagsmithValueType.FLOAT: float,
            # semver.VersionInfo: remove_semver_suffix,
        }.get(self.value_type, str)
