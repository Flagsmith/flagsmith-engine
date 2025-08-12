import typing

import pytest

from flag_engine.segments import constants
from flag_engine.segments.models import SegmentRuleModel
from flag_engine.segments.types import RuleType
from flag_engine.segments.utils import _none


@pytest.mark.parametrize(
    "iterable, expected_result",
    (
        ([], True),
        ([False], True),
        ([False, False], True),
        ([False, True], False),
        ([True, True], False),
    ),
)
def test_segment_rule_none(
    iterable: typing.List[bool],
    expected_result: bool,
) -> None:
    assert SegmentRuleModel.none(iterable) is expected_result


@pytest.mark.parametrize(
    "rule_type, expected_function",
    (
        (constants.ALL_RULE, all),
        (constants.ANY_RULE, any),
        (constants.NONE_RULE, _none),
    ),
)
def test_segment_rule_matching_function(
    rule_type: RuleType,
    expected_function: typing.Callable[[typing.Iterable[object]], bool],
) -> None:
    assert SegmentRuleModel(type=rule_type).matching_function == expected_function
