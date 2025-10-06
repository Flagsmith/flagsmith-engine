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
    ]:
        yield pyjson5.loads((test_cases_dir_path / file_path).read_text())["context"]


TEST_CASES = list(_extract_test_cases(TEST_CASES_PATH))
BENCHMARK_CONTEXTS = list(_extract_benchmark_contexts(TEST_CASES_PATH))


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
