from flag_engine.environments.models import Environment
from flag_engine.features.models import Feature, FeatureState


def get_environment_feature_state_for_feature(
    environment: Environment, feature: Feature
) -> FeatureState:
    return next(filter(lambda fs: fs.feature == feature, environment.feature_states))
