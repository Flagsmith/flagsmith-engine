import typing
from dataclasses import dataclass


@dataclass
class Feature:
    id: int
    name: str

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


@dataclass
class FeatureState:
    feature: Feature
    enabled: bool
    value: typing.Any = None
