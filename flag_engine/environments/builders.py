import typing

from flag_engine.environments.models import EnvironmentModel
from flag_engine.environments.schemas import EnvironmentSchema

environment_schema = EnvironmentSchema()


def build_environment_dict(environment_obj: typing.Any) -> dict:
    return environment_schema.dump(environment_obj)


def build_environment_model(environment_obj: object) -> EnvironmentModel:
    return environment_schema.load(build_environment_dict(environment_obj))
