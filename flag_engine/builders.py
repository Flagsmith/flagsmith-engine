from .models import Environment
from .schemas import EnvironmentSchema

environment_schema = EnvironmentSchema()


def build_environment_model(environment_obj: object) -> Environment:
    environment_data = environment_schema.dump(environment_obj)
    return environment_schema.load(environment_data)
