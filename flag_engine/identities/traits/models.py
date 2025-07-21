from pydantic import BaseModel, Field

from flag_engine.identities.traits.types import ContextValue


class TraitModel(BaseModel):
    trait_key: str
    trait_value: ContextValue = Field(...)
