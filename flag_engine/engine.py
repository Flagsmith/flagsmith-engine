import typing
import warnings

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

__all__ = (
    "get_environment_feature_states",
    "get_environment_feature_state",
    "get_identity_feature_states",
    "get_identity_feature_state",
    "get_evaluation_result",
)


def get_environment_feature_states(
    environment: EnvironmentModel,
) -> typing.List[FeatureStateModel]:
    """
    Get a list of feature states for a given environment

    :param environment: the environment model object
    """
    warnings.warn(
        "`get_environment_feature_states` is deprecated, use `get_evaluation_result` instead.",
        DeprecationWarning,
    )
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
    warnings.warn(
        "`get_environment_feature_state` is deprecated, use `get_evaluation_result` instead.",
        DeprecationWarning,
    )

    for feature_state in environment.feature_states:
        if feature_state.feature.name == feature_name:
            return feature_state

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
    warnings.warn(
        "`get_identity_feature_states` is deprecated, use `get_evaluation_result` instead.",
        DeprecationWarning,
    )
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
    warnings.warn(
        "`get_identity_feature_state` is deprecated, use `get_evaluation_result` instead.",
        DeprecationWarning,
    )
    context = map_environment_identity_to_context(
        environment=environment,
        identity=identity,
        override_traits=override_traits,
    )

    result = get_evaluation_result(context)

    for feature_state in map_flag_results_to_feature_states(result["flags"]):
        if feature_state.feature.name == feature_name:
            return feature_state

    raise FeatureStateNotFound()
