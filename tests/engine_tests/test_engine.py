import typing
from pathlib import Path

import pytest
from pydantic import BaseModel

from flag_engine.engine import get_identity_feature_states
from flag_engine.environments.models import EnvironmentModel
from flag_engine.identities.models import IdentityModel

MODULE_PATH = Path(__file__).parent.resolve()

APIResponse = typing.Dict[str, typing.Any]


class EngineTestCase(BaseModel):
    identity: IdentityModel
    response: APIResponse


class EngineTestData(BaseModel):
    environment: EnvironmentModel
    identities_and_responses: typing.List[EngineTestCase]


def _extract_test_cases(
    file_path: Path,
) -> typing.Iterable[typing.Tuple[EnvironmentModel, IdentityModel, APIResponse]]:
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
        test_data = EngineTestData.model_validate_json(f.read())
        return [
            (test_data.environment, test_case.identity, test_case.response)
            for test_case in test_data.identities_and_responses
        ]


@pytest.mark.parametrize(
    "environment_model, identity_model, api_response",
    _extract_test_cases(
        MODULE_PATH / "engine-test-data/data/environment_n9fbf9h3v4fFgH3U3ngWhb.json"
    ),
)
def test_engine(
    environment_model: EnvironmentModel,
    identity_model: IdentityModel,
    api_response: typing.Dict[str, typing.Any],
) -> None:
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
        assert (
            feature_state.get_value(identity_model.django_id)
            == api_flags[i]["feature_state_value"]
        )
        assert feature_state.enabled == api_flags[i]["enabled"]
