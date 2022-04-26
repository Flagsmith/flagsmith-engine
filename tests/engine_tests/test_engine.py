import json
import typing
from pathlib import Path

import pytest

from flag_engine.engine import get_identity_feature_states
from flag_engine.environments.builders import build_environment_model
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.models import FlagsmithValue, FlagsmithValueType
from flag_engine.identities.builders import build_identity_model
from flag_engine.identities.models import IdentityModel

MODULE_PATH = Path(__file__).parent.resolve()


def _extract_test_cases(
    file_path: Path,
) -> typing.Iterable[typing.Tuple[EnvironmentModel, IdentityModel, dict]]:
    """
    Extract the test cases from the json data file which should be in the following
    format.

        {
          "environment": {...},  // the environment document as found in DynamoDB
          "identities_and_responses": [
            {
              "identity": {...},  // the identity as found in DynamoDB,
              "response": {...},  // the response that was obtained from the current API
            }
          ]
        }

    :param file_path: the path to the json data file
    :return: a list of tuples containing the environment, identity and api response
    """
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
        MODULE_PATH / "engine-test-data/data/environment_n9fbf9h3v4fFgH3U3ngWhb.json"
    ),
)
def test_engine(environment_model, identity_model, api_response):
    # When
    # we get the feature states from the engine
    engine_response = get_identity_feature_states(environment_model, identity_model)

    # and we sort the feature states so we can iterate over them and compare
    sorted_engine_flags = sorted(engine_response, key=lambda fs: fs.feature.name)
    api_flags = api_response["flags"]

    # Then
    # there are an equal number of flags and feature states
    assert len(sorted_engine_flags) == len(api_flags)

    # and the values and enabled status of each of the feature states returned by the
    # engine are identical to those returned by the Django API (i.e. the test data).
    for i, feature_state in enumerate(sorted_engine_flags):
        engine_value = feature_state.get_value(identity_model.django_id)
        api_value = api_flags[i]["feature_state_value"]

        api_value_as_fs_value = FlagsmithValue(
            value=str(api_value),
            value_type=FlagsmithValueType(type(api_value).__name__.lower()),
        )

        assert engine_value == api_value_as_fs_value
        assert feature_state.enabled == api_flags[i]["enabled"]
