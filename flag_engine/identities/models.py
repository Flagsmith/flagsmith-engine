import datetime
import typing
import uuid
from dataclasses import dataclass, field

from flag_engine.identities.traits.models import TraitModel
from flag_engine.utils.collections import IdentityFeaturesList
from flag_engine.utils.datetime import utcnow_with_tz


@dataclass
class IdentityModel:
    identifier: str
    environment_api_key: str
    created_date: datetime = field(default_factory=utcnow_with_tz)
    identity_features: IdentityFeaturesList = field(
        default_factory=IdentityFeaturesList
    )
    identity_traits: typing.List[TraitModel] = field(default_factory=list)
    identity_uuid: str = field(default_factory=uuid.uuid4)
    django_id: int = None

    @property
    def composite_key(self) -> str:
        return self.generate_composite_key(self.environment_api_key, self.identifier)

    @staticmethod
    def generate_composite_key(env_key: str, identifier: str) -> str:
        return f"{env_key}_{identifier}"

    def get_hash_key(self, use_mv_v2_evaluation: bool) -> str:
        return self.composite_key if use_mv_v2_evaluation else self.identifier

    def update_traits(
        self, traits: typing.List[TraitModel]
    ) -> typing.Tuple[typing.List[TraitModel], bool]:
        existing_traits = {trait.trait_key: trait for trait in self.identity_traits}
        traits_changed = False

        for trait in traits:
            existing_trait = existing_traits.get(trait.trait_key)

            if trait.trait_value is None and existing_trait:
                existing_traits.pop(trait.trait_key)
                traits_changed = True

            elif getattr(existing_trait, "trait_value", None) != trait.trait_value:
                existing_traits[trait.trait_key] = trait
                traits_changed = True

        self.identity_traits = list(existing_traits.values())
        return self.identity_traits, traits_changed

    def prune_features(self, valid_feature_names: typing.List[str]) -> None:
        self.identity_features = IdentityFeaturesList(
            [
                fs
                for fs in self.identity_features
                if fs.feature.name in valid_feature_names
            ]
        )
