import typing
from dataclasses import dataclass

from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.models import IdentityModel


@dataclass
class Flag:
    id: int
    feature: FeatureModel
    enabled: bool
    value: typing.Any

    @classmethod
    def from_feature_state(
        cls, feature_state: FeatureStateModel, identity: IdentityModel = None
    ):
        get_value_args = []
        if identity:
            get_value_args.append(identity.django_id or identity.identifier)

        return cls(
            id=feature_state.id,
            feature=feature_state.feature,
            enabled=feature_state.enabled,
            value=feature_state.get_value(*get_value_args),
        )
