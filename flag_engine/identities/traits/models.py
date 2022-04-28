import typing
from dataclasses import dataclass

from flag_engine.utils.models import FlagsmithValue


@dataclass
class TraitModel:
    trait_key: str
    trait_value: FlagsmithValue

    def __init__(self, trait_key: str, trait_value: typing.Any):
        self.trait_key = trait_key
        if not isinstance(trait_value, FlagsmithValue):
            trait_value = FlagsmithValue.from_untyped_value(trait_value)
        self.trait_value = trait_value
