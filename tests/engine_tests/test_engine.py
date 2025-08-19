import typing
from pathlib import Path

import pytest
from pydantic import BaseModel
from pytest_codspeed import BenchmarkFixture  # type: ignore[import-untyped]

from flag_engine.context.mappers import map_environment_identity_to_context
from flag_engine.engine import get_identity_feature_states
from flag_engine.environments.models import EnvironmentModel
from flag_engine.identities.models import IdentityModel
from flag_engine.segments.evaluator import get_evaluation_result

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


TEST_CASES = _extract_test_cases(
    MODULE_PATH / "engine-test-data/data/environment_n9fbf9h3v4fFgH3U3ngWhb.json"
)


@pytest.mark.parametrize(
    "environment_model, identity_model, api_response",
    TEST_CASES,
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
    api_flags = api_response["flags"]

    # Then
    # there are an equal number of flags and feature states
    assert len(engine_response) == len(api_flags)

    # and the values and enabled status of each of the feature states returned by the
    # engine are identical to those returned by the Django API (i.e. the test data).
    assert {
        fs.feature.name: fs.get_value(identity_model.django_id)
        for fs in engine_response
    } == {flag["feature"]["name"]: flag["feature_state_value"] for flag in api_flags}


@pytest.mark.benchmark
def test_engine_benchmark(benchmark: BenchmarkFixture) -> None:  # type: ignore[no-any-unimported]
    contexts = []
    for environment_model, identity_model, _ in TEST_CASES:
        contexts.append(
            map_environment_identity_to_context(
                environment=environment_model,
                identity=identity_model,
                override_traits=None,
            )
        )

    @benchmark
    def __() -> None:
        for context in contexts:
            get_evaluation_result(context)
