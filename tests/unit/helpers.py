from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.models import FeatureModel, FeatureStateModel


def get_environment_feature_state_for_feature(
    environment: EnvironmentModel, feature: FeatureModel
) -> FeatureStateModel:
    return next(filter(lambda fs: fs.feature == feature, environment.feature_states))
