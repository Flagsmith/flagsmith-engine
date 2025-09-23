import json
import typing
from pathlib import Path

import pytest

from flag_engine.context.types import EvaluationContext
from flag_engine.engine import get_evaluation_result
from flag_engine.result.types import EvaluationResult

MODULE_PATH = Path(__file__).parent.resolve()

EnvironmentDocument = dict[str, typing.Any]


def _extract_test_cases(
    file_path: Path,
) -> typing.Iterable[tuple[EvaluationContext, EvaluationResult]]:
    test_data = json.loads(file_path.read_text())

    for case in test_data["test_cases"]:
        context: EvaluationContext = case["context"]
        result: EvaluationResult = case["result"]
        yield context, result


TEST_CASES = list(
    _extract_test_cases(
        MODULE_PATH / "engine-test-data/data/environment_n9fbf9h3v4fFgH3U3ngWhb.json"
    )
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
    for context, _ in TEST_CASES:
        get_evaluation_result(context)
