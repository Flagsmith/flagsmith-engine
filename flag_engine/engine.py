import typing

from flag_engine.context.mappers import (
    map_environment_identity_to_context,
    map_flag_results_to_feature_states,
)
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.models import FeatureStateModel
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.segments.evaluator import get_evaluation_result
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

    result = get_evaluation_result(context)

    feature_states = map_flag_results_to_feature_states(result["flags"])

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

    result = get_evaluation_result(context)

    feature_states = map_flag_results_to_feature_states(result["flags"])

    matching_feature_state = next(
        filter(
            lambda feature_state: feature_state.feature.name == feature_name,
            feature_states,
        ),
        None,
    )

    if not matching_feature_state:
        raise FeatureStateNotFound()

    return matching_feature_state
