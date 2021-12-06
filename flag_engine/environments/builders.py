from flag_engine.environments.models import EnvironmentModel
from flag_engine.environments.schemas import EnvironmentSchema

environment_schema = EnvironmentSchema()


def build_environment_model(environment_dict: dict) -> EnvironmentModel:
    return environment_schema.load(environment_dict)
