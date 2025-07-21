import typing

from flag_engine.context.mappers import map_environment_identity_to_context
from flag_engine.context.types import EvaluationContext
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.segments.evaluator import get_context_segments
from flag_engine.utils.exceptions import FeatureStateNotFound


def get_environment_feature_states(
    environment: EnvironmentModel,
) -> typing.List[FeatureStateModel]:
    """
    Get a list of feature states for a given environment

    :param environment: the environment model object
    """
    if environment.get_hide_disabled_flags():
        return [fs for fs in environment.feature_states if fs.enabled]
    return environment.feature_states


def get_environment_feature_state(
    environment: EnvironmentModel, feature_name: str
) -> FeatureStateModel:
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
    override_traits: typing.Optional[typing.List[TraitModel]] = None,
) -> typing.List[FeatureStateModel]:
    """
    Get a list of feature states for a given identity in a given environment.

    :param environment: the environment model object the identity belongs to
    :param identity: the identity model object to get the feature state for
    :param override_traits: optionally override the traits on the identity model
    :return: list of feature state models based on the environment, any matching
        segments and any specific identity overrides
    """
    context = map_environment_identity_to_context(
        environment=environment,
        identity=identity,
        override_traits=override_traits,
    )

    feature_states = list(
        _get_identity_feature_states_dict(
            environment=environment,
            identity=identity,
            context=context,
        ).values()
    )
    if environment.get_hide_disabled_flags():
        return [fs for fs in feature_states if fs.enabled]
    return feature_states


def get_identity_feature_state(
    environment: EnvironmentModel,
    identity: IdentityModel,
    feature_name: str,
    override_traits: typing.Optional[typing.List[TraitModel]] = None,
) -> FeatureStateModel:
    """
    Get a specific feature state for a given identity in a given environment.

    :param environment: the environment model object the identity belongs to
    :param identity: the identity model object to get the feature state for
    :param feature_name: the name of the feature to get the feature state for
    :param override_traits: optionally override the traits on the identity model
    :return: feature state model based on the environment, any matching
        segments and any specific identity overrides
    """
    context = map_environment_identity_to_context(
        environment=environment,
        identity=identity,
        override_traits=override_traits,
    )

    feature_states = _get_identity_feature_states_dict(
        environment=environment,
        identity=identity,
        context=context,
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
    context: EvaluationContext,
) -> typing.Dict[FeatureModel, FeatureStateModel]:
    # Get feature states from the environment
    feature_states_by_feature = {fs.feature: fs for fs in environment.feature_states}

    # Override with any feature states defined by matching segments
    for context_segment in get_context_segments(
        context=context,
        segments=environment.project.segments,
    ):
        for segment_feature_state in context_segment.feature_states:
            if (
                feature_state := feature_states_by_feature.get(
                    segment_feature := segment_feature_state.feature
                )
            ) and feature_state.is_higher_segment_priority(segment_feature_state):
                continue
            feature_states_by_feature[segment_feature] = segment_feature_state

    # Override with any feature states defined directly the identity
    feature_states_by_feature.update(
        {
            identity_feature: identity_feature_state
            for identity_feature_state in identity.identity_features
            if (identity_feature := identity_feature_state.feature)
            in feature_states_by_feature
        }
    )

    return feature_states_by_feature
