from typing import Any, Union, get_args

from pydantic import BaseModel, Field
from typing_extensions import TypeGuard

from flag_engine.identities.traits.types import TraitValue

UnconstrainedTraitValue = Union[None, int, float, bool, str]


def _is_trait_value(value: Any) -> TypeGuard[UnconstrainedTraitValue]:
    return isinstance(value, get_args(UnconstrainedTraitValue))


class TraitModel(BaseModel):
    trait_key: str
    trait_value: TraitValue = Field(...)
