import typing

from flag_engine.environments.models import EnvironmentModel
from flag_engine.environments.schemas import (
    EnvironmentSchemaDump,
    EnvironmentSchemaLoad,
)

environment_schema_dump = EnvironmentSchemaDump()
environment_schema_load = EnvironmentSchemaLoad()


def build_environment_dict(environment_obj: typing.Any) -> dict:
    return environment_schema_dump.dump(environment_obj)


def build_environment_model(environment_obj: typing.Any) -> EnvironmentModel:
    return environment_schema_load.load(build_environment_dict(environment_obj))
