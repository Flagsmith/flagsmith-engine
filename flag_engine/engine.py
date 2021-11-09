import typing

from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.models import IdentityModel, TraitModel
from flag_engine.segments.evaluator import evaluate_identity_in_segment


def get_identity_feature_states(
    environment: EnvironmentModel,
    identity: IdentityModel,
    override_traits: typing.List[TraitModel] = None,
) -> typing.List[FeatureStateModel]:
    """
    Get a list of feature states for a given identity in a given environment.

    :param environment: the environment model object the identity belongs to
    :param identity: the identity model object to get the feature state for
    :param override_traits: optionally override the traits on the identity model
    :return: list of feature state models based on the environment, any matching
        segments and any specific identity overrides
    """
    return list(
        _get_identity_feature_states_dict(
            environment, identity, override_traits
        ).values()
    )


def get_identity_feature_state(
    environment: EnvironmentModel,
    identity: IdentityModel,
    feature_name: str,
    override_traits: typing.List[TraitModel] = None,
):
    """
    Get a specific feature state for a given identity in a given environment.

    :param environment: the environment model object the identity belongs to
    :param identity: the identity model object to get the feature state for
    :param feature_name: the name of the feature to get the feature state for
    :param override_traits: optionally override the traits on the identity model
    :return: feature state model based on the environment, any matching
        segments and any specific identity overrides
    """
    feature_states = _get_identity_feature_states_dict(
        environment, identity, override_traits
    )
    matching_feature = next(
        filter(lambda feature: feature.name == feature_name, feature_states.keys())
    )
    return feature_states[matching_feature]


def _get_identity_feature_states_dict(
    environment: EnvironmentModel,
    identity: IdentityModel,
    override_traits: typing.Optional[typing.List[TraitModel]],
) -> typing.Dict[FeatureModel, FeatureStateModel]:
    # Get feature states from the environment
    feature_states = {fs.feature: fs for fs in environment.feature_states}

    # Override with any feature states defined by matching segments
    for feature_state in environment.segment_overrides:
        segment = environment.get_segment(feature_state.segment_id)
        if feature_state.feature in feature_states and evaluate_identity_in_segment(
            identity, segment, override_traits
        ):
            feature_states[feature_state.feature] = feature_state

    # Override with any feature states defined directly the identity
    feature_states.update(
        {
            fs.feature: fs
            for fs in identity.identity_features
            if fs.feature in feature_states
        }
    )

    return feature_states