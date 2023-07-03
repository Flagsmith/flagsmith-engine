from pydantic import BaseModel

from flag_engine.identities.traits.types import TraitValue


class TraitModel(BaseModel):
    trait_key: str
    trait_value: TraitValue = ...

    class Config:
        smart_union: bool = True
