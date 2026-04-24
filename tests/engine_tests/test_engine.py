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
LARGE_ENVIRONMENT_TEST_CASE = (
    "test_000000cf-0000-0000-0000-000000000000__large_environment.json"
)

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


def _load_test_case_context(name: str) -> EvaluationContext:
    ctx: EvaluationContext = pyjson5.loads((TEST_CASES_PATH / name).read_text())[
        "context"
    ]
    return ctx


TEST_CASES = sorted(
    _extract_test_cases(TEST_CASES_PATH),
    key=lambda param: str(param.id),
)
BENCHMARK_CONTEXTS = list(_extract_benchmark_contexts(TEST_CASES_PATH))
LARGE_BENCHMARK_CONTEXT = _load_test_case_context(LARGE_ENVIRONMENT_TEST_CASE)


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
