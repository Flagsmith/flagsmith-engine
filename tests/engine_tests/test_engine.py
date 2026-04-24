import typing
from itertools import chain
from pathlib import Path

import pyjson5
import pytest
from _pytest.mark import ParameterSet

from flag_engine.context.types import EvaluationContext, FeatureContext
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


def _build_large_benchmark_context(
    n_features: int = 262,
    multivariate_features: int = 26,
) -> EvaluationContext:
    """Mirror the scenario from flagsmith-python-client issue #198: a real-world
    local-evaluation environment with ~260 features, a handful of which use
    multivariate splits, evaluated for a single identity. Small enough to
    keep the benchmark fast but large enough to surface per-feature overhead.
    """
    features: dict[str, FeatureContext[typing.Any]] = {}
    for i in range(n_features):
        name = f"feature_{i:04d}"
        fc: FeatureContext[typing.Any] = {
            "key": str(i + 1),
            "name": name,
            "enabled": bool(i % 2),
            "value": f"value-{i}",
            "metadata": {"id": i + 1},
        }
        if i < multivariate_features:
            # Intentionally reverse-ordered so ``sorted()`` has work to do.
            fc["variants"] = [
                {"value": f"mv-{i}-b", "weight": 40.0, "priority": 2},
                {"value": f"mv-{i}-a", "weight": 60.0, "priority": 1},
            ]
        features[name] = fc
    return {
        "environment": {"key": "bench-env", "name": "bench"},
        "features": features,
        "segments": {
            "1": {
                "key": "1",
                "name": "bench-segment",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {
                                "property": "venue_id",
                                "operator": "EQUAL",
                                "value": "no-match",
                            }
                        ],
                    }
                ],
            }
        },
        "identity": {
            "identifier": "anonymous",
            "traits": {"venue_id": "12345"},
        },
    }


TEST_CASES = sorted(
    _extract_test_cases(TEST_CASES_PATH),
    key=lambda param: str(param.id),
)
BENCHMARK_CONTEXTS = list(_extract_benchmark_contexts(TEST_CASES_PATH))
LARGE_BENCHMARK_CONTEXT = _build_large_benchmark_context()


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
def test_engine_benchmark_large_context() -> None:
    get_evaluation_result(LARGE_BENCHMARK_CONTEXT)
