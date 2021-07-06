from flag_engine.environments.models import EnvironmentModel
from flag_engine.environments.schemas import EnvironmentSchema

environment_schema = EnvironmentSchema()


def build_environment_model(environment_obj: object) -> EnvironmentModel:
    environment_data = environment_schema.dump(environment_obj)
    return environment_schema.load(environment_data)
