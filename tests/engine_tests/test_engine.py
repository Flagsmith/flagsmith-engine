import typing
from itertools import chain
from pathlib import Path

import pyjson5
import pytest
from _pytest.mark import ParameterSet

from flag_engine.context.types import EvaluationContext
from flag_engine.engine import get_evaluation_result
from flag_engine.result.types import EvaluationResult

TEST_CASES_PATH = Path(__file__).parent / "engine-test-data/test_cases"

EnvironmentDocument = dict[str, typing.Any]


def _extract_test_cases(
    test_cases_dir_path: Path,
) -> typing.Iterable[ParameterSet]:
    for file_path in chain(
        test_cases_dir_path.glob("*.json"),
        test_cases_dir_path.glob("*.jsonc"),
    ):
        test_data = pyjson5.loads(file_path.read_text())
        yield pytest.param(
            test_data["context"],
            test_data["result"],
            id=file_path.stem,
        )


def _extract_benchmark_contexts(
    test_cases_dir_path: Path,
) -> typing.Iterable[EvaluationContext]:
    for file_path in [
        "test_0cfd0d72-4de4-4ed7-9cfb-d80dc3dacead__default.json",
        "test_1bde8445-ca19-4bda-a9d5-3543a800fc0f__context_values.json",
        "test_in_condition_json_array_format__should_match.jsonc",
        "test_in_condition_numeric_comma_separated__should_match.jsonc",
        "test_in_condition_array_matching_value__should_match.jsonc",
    ]:
        yield pyjson5.loads((test_cases_dir_path / file_path).read_text())["context"]


def _build_large_context() -> EvaluationContext:
    """
    An identity evaluation context shaped like a large real-world environment,
    as built by the Python SDK in local evaluation mode.

    262 features, a tenth of them multivariate, and 20 segments with nested
    trait rules, each overriding 5 features. Plus segments on an environment
    context value and on the identifier, as identity overrides are mapped.
    """
    features: dict[str, typing.Any] = {}
    for i in range(1, 263):
        feature: dict[str, typing.Any] = {
            "key": str(i),
            "name": f"feature_{i}",
            "enabled": i % 3 != 0,
            "value": f"value-{i}",
            "metadata": {"id": i},
        }
        if i % 10 == 0:
            feature["variants"] = [
                {"value": f"variant-{k}", "weight": 30, "priority": k, "key": f"v{k}"}
                for k in range(2)
            ]
        features[feature["name"]] = feature

    def override(feature_id: int, value: str, priority: float) -> typing.Any:
        return {
            **features[f"feature_{feature_id}"],
            "enabled": True,
            "value": value,
            "priority": priority,
        }

    segments: dict[str, typing.Any] = {
        str(s): {
            "key": str(s),
            "name": f"segment_{s}",
            "rules": [
                {
                    "type": "ALL",
                    "rules": [
                        {
                            "type": "ANY",
                            "conditions": [
                                {
                                    "property": "plan",
                                    "operator": "EQUAL",
                                    "value": f"plan-{s}",
                                },
                                {
                                    "property": "age",
                                    "operator": "GREATER_THAN",
                                    "value": str(s * 3),
                                },
                            ],
                        },
                        {
                            "type": "ALL",
                            "conditions": [
                                {
                                    "property": "country",
                                    "operator": "IN",
                                    "value": "GB,US,DE,FR",
                                },
                            ],
                        },
                    ],
                }
            ],
            "overrides": [
                override((s * 13 + k * 51) % 262 + 1, f"segment-{s}", s)
                for k in range(5)
            ],
        }
        for s in range(1, 21)
    }
    segments["environment"] = {
        "key": "environment",
        "name": "environment",
        "rules": [
            {
                "type": "ALL",
                "conditions": [
                    {
                        "property": "$.environment.name",
                        "operator": "EQUAL",
                        "value": "Production",
                    },
                ],
            }
        ],
        "overrides": [override(7, "environment", 0)],
    }
    segments["identity_overrides"] = {
        "key": "identity_overrides",
        "name": "identity_overrides",
        "rules": [
            {
                "type": "ALL",
                "conditions": [
                    {
                        "property": "$.identity.identifier",
                        "operator": "IN",
                        "value": ["user-1"],
                    },
                ],
            }
        ],
        "overrides": [override(11, "identity", float("-inf"))],
    }
    return {
        "environment": {"key": "environment-key", "name": "Production"},
        "identity": {
            "identifier": "user-1",
            "key": "environment-key_user-1",
            "traits": {"plan": "plan-7", "age": 30, "country": "GB"},
        },
        "features": features,
        "segments": segments,
    }


def _build_single_feature_context(
    context: EvaluationContext,
    feature_name: str,
) -> EvaluationContext:
    """
    A context trimmed to one feature and the segments overriding it, as the
    Python SDK evaluates a single flag lazily.
    """
    segments = context.get("segments") or {}
    return {
        **context,
        "features": {feature_name: (context.get("features") or {})[feature_name]},
        "segments": {
            key: segment
            for key, segment in segments.items()
            if any(o["name"] == feature_name for o in segment.get("overrides") or ())
        },
    }


TEST_CASES = sorted(
    _extract_test_cases(TEST_CASES_PATH),
    key=lambda param: str(param.id),
)
BENCHMARK_CONTEXTS = list(_extract_benchmark_contexts(TEST_CASES_PATH))
LARGE_BENCHMARK_CONTEXT = _build_large_context()
SINGLE_FEATURE_BENCHMARK_CONTEXT = _build_single_feature_context(
    LARGE_BENCHMARK_CONTEXT, "feature_14"
)


@pytest.mark.parametrize(
    "context, expected_result",
    TEST_CASES,
)
def test_engine(
    context: EvaluationContext,
    expected_result: EvaluationResult,
) -> None:
    # When
    result = get_evaluation_result(context)

    # Then
    assert result == expected_result


@pytest.mark.benchmark
def test_engine_benchmark() -> None:
    for context in BENCHMARK_CONTEXTS:
        get_evaluation_result(context)


@pytest.mark.benchmark
def test_engine_benchmark__large_context() -> None:
    get_evaluation_result(LARGE_BENCHMARK_CONTEXT)


@pytest.mark.benchmark
def test_engine_benchmark__single_feature_context() -> None:
    get_evaluation_result(SINGLE_FEATURE_BENCHMARK_CONTEXT)
