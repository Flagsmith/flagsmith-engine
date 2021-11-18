import datetime
import typing
from dataclasses import dataclass, field

from flag_engine.features.models import FeatureStateModel


@dataclass
class TraitModel:
    trait_key: str
    trait_value: typing.Any


@dataclass
class IdentityModel:
    identifier: str
    environment_api_key: str
    created_date: datetime = field(default_factory=datetime.datetime.now)
    identity_features: typing.List[FeatureStateModel] = field(default_factory=list)
    identity_traits: typing.List[TraitModel] = field(default_factory=list)

    @property
    def composite_key(self):
        return self.generate_composite_key(self.environment_api_key, self.identifier)

    @staticmethod
    def generate_composite_key(env_key: str, identifier: str) -> str:
        return f"{env_key}_{identifier}"
