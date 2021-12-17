import json
import typing

import pytest

from flag_engine.engine import get_identity_feature_states
from flag_engine.environments.builders import build_environment_model
from flag_engine.environments.models import EnvironmentModel
from flag_engine.identities.builders import build_identity_model
from flag_engine.identities.models import IdentityModel


def _extract_test_cases(
    file_path: str,
) -> typing.Iterable[typing.Tuple[EnvironmentModel, IdentityModel, dict]]:
    with open(file_path, "r") as f:
        test_data = json.loads(f.read())
        environment_model = build_environment_model(test_data["environment"])
        return [
            (
                environment_model,
                build_identity_model(test_case["identity"]),
                test_case["response"],
            )
            for test_case in test_data["identities_and_responses"]
        ]


@pytest.mark.parametrize(
    "environment_model, identity_model, api_response",
    _extract_test_cases(
        "engine-test-data/data/environment_n9fbf9h3v4fFgH3U3ngWhb.json"
    ),
)
def test_engine(environment_model, identity_model, api_response):
    # When
    engine_response = get_identity_feature_states(environment_model, identity_model)

    # Then
    sorted_engine_flags = sorted(engine_response, key=lambda fs: fs.feature.name)
    sorted_api_flags = sorted(api_response["flags"], key=lambda f: f["feature"]["name"])

    for i, feature_state in enumerate(sorted_engine_flags):
        assert (
            feature_state.get_value(identity_model.django_id)
            == sorted_api_flags[i]["feature_state_value"]
        )
        assert feature_state.enabled == sorted_api_flags[i]["enabled"]
