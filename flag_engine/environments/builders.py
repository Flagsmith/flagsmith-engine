from flag_engine.environments.models import EnvironmentAPIKeyModel, EnvironmentModel


def build_environment_model(environment_dict: dict) -> EnvironmentModel:
    return EnvironmentModel.parse_obj(environment_dict)


def build_environment_api_key_model(
    environment_key_dict: dict,
) -> EnvironmentAPIKeyModel:
    return EnvironmentAPIKeyModel.parse_obj(environment_key_dict)
