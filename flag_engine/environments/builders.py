from flag_engine.environments.models import EnvironmentAPIKeyModel, EnvironmentModel
from flag_engine.environments.schemas import EnvironmentAPIKeySchema, EnvironmentSchema

environment_schema = EnvironmentSchema()
environment_api_key_schema = EnvironmentAPIKeySchema()


def build_environment_model(environment_dict: dict) -> EnvironmentModel:
    return environment_schema.load(environment_dict)


def build_environment_api_key_model(
    environment_key_dict: dict,
) -> EnvironmentAPIKeyModel:
    return environment_api_key_schema.load(environment_key_dict)
