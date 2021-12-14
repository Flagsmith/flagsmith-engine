import datetime
import typing
import uuid
from collections import UserList
from dataclasses import dataclass, field

from flag_engine.features.models import FeatureStateModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.utils.exceptions import DuplicateFeatureState


class IdentityFeaturesList(UserList):
    def append(self, feature_state: FeatureStateModel):
        if [fs for fs in self.data if fs.feature.id == feature_state.feature.id]:
            raise DuplicateFeatureState("feature state for this feature already exists")

        super().append(feature_state)


@dataclass
class IdentityModel:
    identifier: str
    environment_api_key: str
    created_date: datetime = field(default_factory=datetime.datetime.now)
    identity_features: IdentityFeaturesList[FeatureStateModel] = field(
        default_factory=IdentityFeaturesList
    )
    identity_traits: typing.List[TraitModel] = field(default_factory=list)
    identity_uuid: str = field(default_factory=uuid.uuid4)
    django_id: int = None

    @property
    def composite_key(self):
        return self.generate_composite_key(self.environment_api_key, self.identifier)

    @staticmethod
    def generate_composite_key(env_key: str, identifier: str) -> str:
        return f"{env_key}_{identifier}"

    def update_traits(self, traits: typing.List[TraitModel]) -> None:
        existing_traits = {trait.trait_key: trait for trait in self.identity_traits}

        for trait in traits:
            if trait.trait_value is None:
                existing_traits.pop(trait.trait_key, None)
            else:
                existing_traits[trait.trait_key] = trait

        self.identity_traits = list(existing_traits.values())
