import typing

from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.segments.evaluator import get_identity_segments
from flag_engine.utils.exceptions import FeatureStateNotFound


def get_environment_feature_states(environment: EnvironmentModel):
    """
    Get a list of feature states for a given environment

    :param environment: the environment model object
    """
    if environment.project.hide_disabled_flags:
        return [fs for fs in environment.feature_states if fs.enabled]
    return environment.feature_states


def get_environment_feature_state(environment: EnvironmentModel, feature_name: str):
    """
    Get a specific feature state for a given feature_name in a given environment

    :param environment: the environment model object
    :param feature_name: the name of the feature to get the feature state for
    """
    try:
        return next(
            filter(lambda f: f.feature.name == feature_name, environment.feature_states)
        )

    except StopIteration:
        raise FeatureStateNotFound()


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
    feature_states = list(
        _get_identity_feature_states_dict(
            environment, identity, override_traits
        ).values()
    )
    if environment.project.hide_disabled_flags:
        return [fs for fs in feature_states if fs.enabled]
    return feature_states


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
        filter(lambda feature: feature.name == feature_name, feature_states.keys()),
        None,
    )

    if not matching_feature:
        raise FeatureStateNotFound()

    return feature_states[matching_feature]


def _get_identity_feature_states_dict(
    environment: EnvironmentModel,
    identity: IdentityModel,
    override_traits: typing.Optional[typing.List[TraitModel]],
) -> typing.Dict[FeatureModel, FeatureStateModel]:
    # Get feature states from the environment
    feature_states = {fs.feature: fs for fs in environment.feature_states}

    # Override with any feature states defined by matching segments
    identity_segments = get_identity_segments(environment, identity, override_traits)
    for matching_segment in identity_segments:
        for feature_state in matching_segment.feature_states:
            if feature_state.feature in feature_states:
                if feature_states[feature_state.feature].is_higher_segment_priority(
                    feature_state
                ):
                    continue
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
