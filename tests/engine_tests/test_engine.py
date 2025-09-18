import json
import typing
from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from flag_engine.context.types import EvaluationContext, FeatureContext, SegmentRule
from flag_engine.engine import get_evaluation_result

MODULE_PATH = Path(__file__).parent.resolve()

EnvironmentDocument = dict[str, typing.Any]
APIResponse = dict[str, typing.Any]


@dataclass
class EngineTestCase:
    context: EvaluationContext
    response: APIResponse


def _extract_test_cases(
    file_path: Path,
) -> typing.Iterable[tuple[EvaluationContext, APIResponse]]:
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
    test_data = json.loads(file_path.read_text())

    environment_document = test_data["environment"]

    def _extract_segment_rules(rules: list[dict[str, typing.Any]]) -> list[SegmentRule]:
        return [
            {
                "type": rule["type"],
                "conditions": [
                    {
                        "property": condition.get("property_"),
                        "operator": condition["operator"],
                        "value": condition["value"],
                    }
                    for condition in rule.get("conditions", [])
                ],
                "rules": _extract_segment_rules(rule.get("rules", [])),
            }
            for rule in rules
        ]

    def _extract_feature_contexts(
        feature_states: list[dict[str, typing.Any]],
    ) -> typing.Iterable[FeatureContext]:
        for feature_state in feature_states:
            feature_context = FeatureContext(
                key=str(feature_state["django_id"]),
                feature_key=str(feature_state["feature"]["id"]),
                name=feature_state["feature"]["name"],
                enabled=feature_state["enabled"],
                value=feature_state["feature_state_value"],
            )
            if multivariate_feature_state_values := feature_state.get(
                "multivariate_feature_state_values"
            ):
                feature_context["variants"] = [
                    {
                        "value": multivariate_feature_state_value[
                            "multivariate_feature_option"
                        ]["value"],
                        "weight": multivariate_feature_state_value[
                            "percentage_allocation"
                        ],
                    }
                    for multivariate_feature_state_value in sorted(
                        multivariate_feature_state_values,
                        key=itemgetter("id"),
                    )
                ]
            if (feature_segment := feature_state.get("feature_segment")) and (
                priority := feature_segment.get("priority")
            ) is not None:
                feature_context["priority"] = priority

            yield feature_context

    for case in test_data["identities_and_responses"]:
        identity_data = case["identity"]
        response = case["response"]

        context: EvaluationContext = {
            "environment": {
                "key": environment_document["api_key"],
                "name": "Test Environment",
            },
            "features": {
                feature["name"]: feature
                for feature in _extract_feature_contexts(
                    environment_document["feature_states"]
                )
            },
            "segments": {
                str(segment["id"]): {
                    "key": str(segment["id"]),
                    "name": segment["name"],
                    "rules": _extract_segment_rules(segment["rules"]),
                    "overrides": [
                        *_extract_feature_contexts(segment.get("feature_states", []))
                    ],
                }
                for segment in environment_document["project"]["segments"]
            },
            "identity": {
                "identifier": identity_data["identifier"],
                "key": identity_data.get("django_id") or identity_data["composite_key"],
                "traits": {
                    trait["trait_key"]: trait["trait_value"]
                    for trait in identity_data["identity_traits"]
                },
            },
        }

        yield context, response


TEST_CASES = list(
    _extract_test_cases(
        MODULE_PATH / "engine-test-data/data/environment_n9fbf9h3v4fFgH3U3ngWhb.json"
    )
)


@pytest.mark.parametrize(
    "context, response",
    TEST_CASES,
)
def test_engine(
    context: EvaluationContext,
    response: APIResponse,
    mocker: MockerFixture,
) -> None:
    # When
    engine_response = get_evaluation_result(context)

    # Then
    assert {flag["feature_key"]: flag for flag in engine_response["flags"]} == {
        (feature_key := str(flag["feature"]["id"])): {
            "name": flag["feature"]["name"],
            "feature_key": feature_key,
            "enabled": flag["enabled"],
            "value": flag["feature_state_value"],
            "reason": mocker.ANY,
        }
        for flag in response["flags"]
    }


@pytest.mark.benchmark
def test_engine_benchmark() -> None:
    for context, _ in TEST_CASES:
        get_evaluation_result(context)
