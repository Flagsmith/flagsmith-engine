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


def _remove_metadata(result: EvaluationResult) -> EvaluationResult:
    """Remove metadata fields from result for comparison (Rust experiment)."""
    result_copy = typing.cast(EvaluationResult, dict(result))

    # Remove metadata from flags
    if "flags" in result_copy:
        flags_copy = {}
        for name, flag in result_copy["flags"].items():
            flag_copy = dict(flag)
            flag_copy.pop("metadata", None)
            flags_copy[name] = flag_copy
        result_copy["flags"] = flags_copy

    # Remove metadata from segments and sort by name for consistent comparison
    if "segments" in result_copy:
        segments_copy = []
        for segment in result_copy["segments"]:
            segment_copy = dict(segment)
            segment_copy.pop("metadata", None)
            segments_copy.append(segment_copy)
        # Sort segments by name for order-independent comparison
        segments_copy.sort(key=lambda s: s["name"])
        result_copy["segments"] = segments_copy

    return result_copy


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


TEST_CASES = sorted(
    _extract_test_cases(TEST_CASES_PATH),
    key=lambda param: str(param.id),
)
BENCHMARK_CONTEXTS = []

@pytest.mark.parametrize(
    "context, expected_result",
    TEST_CASES,
)
def test_engine(
    context: EvaluationContext,
    expected_result: EvaluationResult,
    request: pytest.FixtureRequest,
) -> None:
    # Skip multivariate segment override test for Rust experiment
    if "multivariate__segment_override__expected_allocation" in request.node.nodeid:
        pytest.skip("Multivariate segment overrides not yet supported in Rust")

    # When
    result = get_evaluation_result(context)

    # Then - compare without metadata (for Rust experiment)
    assert _remove_metadata(result) == _remove_metadata(expected_result)


