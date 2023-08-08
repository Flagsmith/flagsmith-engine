from decimal import Decimal
from typing import Any, get_args

from pydantic import BaseModel, validator

from flag_engine.identities.traits.types import TraitValue

TRAIT_VALUE_TYPES = get_args(TraitValue)


class TraitModel(BaseModel):
    trait_key: str
    trait_value: TraitValue = ...

    @validator("trait_value", pre=True)
    def convert_trait_value(cls, value: Any) -> TraitValue:
        if isinstance(value, TRAIT_VALUE_TYPES):
            return value
        if isinstance(value, Decimal) and not value.as_tuple().exponent:
            return int(value)
        return str(value)

    class Config:
        smart_union: bool = True
