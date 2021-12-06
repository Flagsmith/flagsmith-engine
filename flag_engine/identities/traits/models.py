import typing
from dataclasses import dataclass


@dataclass
class TraitModel:
    trait_key: str
    trait_value: typing.Any
