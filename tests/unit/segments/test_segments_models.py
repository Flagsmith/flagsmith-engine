import typing

import pytest

from flag_engine.segments import constants
from flag_engine.segments.models import SegmentRuleModel
from flag_engine.segments.types import RuleType
from flag_engine.segments.utils import none


@pytest.mark.parametrize(
    "rule_type, expected_function",
    (
        (constants.ALL_RULE, all),
        (constants.ANY_RULE, any),
        (constants.NONE_RULE, none),
    ),
)
def test_segment_rule_matching_function(
    rule_type: RuleType,
    expected_function: typing.Callable[[typing.Iterable[object]], bool],
) -> None:
    assert SegmentRuleModel(type=rule_type).matching_function is expected_function
