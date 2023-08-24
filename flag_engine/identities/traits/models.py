from decimal import Decimal
from typing import Any, Union, get_args

from pydantic import BaseModel, Field, field_validator
from typing_extensions import TypeGuard

from flag_engine.identities.traits.types import TraitValue

UnconstrainedTraitValue = Union[None, int, float, bool, str]


def _is_trait_value(value: Any) -> TypeGuard[UnconstrainedTraitValue]:
    return isinstance(value, get_args(UnconstrainedTraitValue))


class TraitModel(BaseModel):
    trait_key: str
    trait_value: TraitValue = Field(...)

    @field_validator("trait_value", mode="before")
    def convert_trait_value(cls, value: Any) -> UnconstrainedTraitValue:
        if _is_trait_value(value):
            return value
        if isinstance(value, Decimal) and not value.as_tuple().exponent:
            return int(value)
        return str(value)
