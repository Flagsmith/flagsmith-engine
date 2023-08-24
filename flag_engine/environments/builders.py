from typing import Any, Dict

from flag_engine.environments.models import EnvironmentAPIKeyModel, EnvironmentModel


def build_environment_model(environment_dict: Dict[str, Any]) -> EnvironmentModel:
    return EnvironmentModel.model_validate(environment_dict)


def build_environment_api_key_model(
    environment_key_dict: Dict[str, Any],
) -> EnvironmentAPIKeyModel:
    return EnvironmentAPIKeyModel.model_validate(environment_key_dict)
