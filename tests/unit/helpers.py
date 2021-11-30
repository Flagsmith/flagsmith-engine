from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.models import FeatureModel, FeatureStateModel


def get_environment_feature_state_for_feature(
    environment: EnvironmentModel, feature: FeatureModel
) -> FeatureStateModel:
    return next(filter(lambda fs: fs.feature == feature, environment.feature_states))


def get_environment_feature_state_for_feature_by_name(
    environment: EnvironmentModel, feature_name: str
) -> FeatureStateModel:
    return next(
        filter(lambda fs: fs.feature.name == feature_name, environment.feature_states)
    )
