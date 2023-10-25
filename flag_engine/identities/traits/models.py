from pydantic import BaseModel, Field

from flag_engine.identities.traits.types import TraitValue


class TraitModel(BaseModel):
    trait_key: str
    trait_value: TraitValue = Field(...)
