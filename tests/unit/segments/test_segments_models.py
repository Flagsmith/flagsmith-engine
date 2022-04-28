import pytest

from flag_engine.segments import constants
from flag_engine.segments.models import SegmentConditionModel, SegmentRuleModel
from flag_engine.utils.models import FlagsmithValue


@pytest.mark.parametrize(
    "operator, trait_value, condition_value, expected_result",
    (
        (constants.EQUAL, "bar", "bar", True),
        (constants.EQUAL, "bar", "baz", False),
        (constants.EQUAL, 1, "1", True),
        (constants.EQUAL, 1, "2", False),
        (constants.EQUAL, True, "True", True),
        (constants.EQUAL, False, "False", True),
        (constants.EQUAL, False, "True", False),
        (constants.EQUAL, True, "False", False),
        (constants.EQUAL, 1.23, "1.23", True),
        (constants.EQUAL, 1.23, "4.56", False),
        (constants.GREATER_THAN, 2, "1", True),
        (constants.GREATER_THAN, 1, "1", False),
        (constants.GREATER_THAN, 0, "1", False),
        (constants.GREATER_THAN, 2.1, "2.0", True),
        (constants.GREATER_THAN, 2.1, "2.1", False),
        (constants.GREATER_THAN, 2.0, "2.1", False),
        (constants.GREATER_THAN_INCLUSIVE, 2, "1", True),
        (constants.GREATER_THAN_INCLUSIVE, 1, "1", True),
        (constants.GREATER_THAN_INCLUSIVE, 0, "1", False),
        (constants.GREATER_THAN_INCLUSIVE, 2.1, "2.0", True),
        (constants.GREATER_THAN_INCLUSIVE, 2.1, "2.1", True),
        (constants.GREATER_THAN_INCLUSIVE, 2.0, "2.1", False),
        (constants.LESS_THAN, 1, "2", True),
        (constants.LESS_THAN, 1, "1", False),
        (constants.LESS_THAN, 1, "0", False),
        (constants.LESS_THAN, 2.0, "2.1", True),
        (constants.LESS_THAN, 2.1, "2.1", False),
        (constants.LESS_THAN, 2.1, "2.0", False),
        (constants.LESS_THAN_INCLUSIVE, 1, "2", True),
        (constants.LESS_THAN_INCLUSIVE, 1, "1", True),
        (constants.LESS_THAN_INCLUSIVE, 1, "0", False),
        (constants.LESS_THAN_INCLUSIVE, 2.0, "2.1", True),
        (constants.LESS_THAN_INCLUSIVE, 2.1, "2.1", True),
        (constants.LESS_THAN_INCLUSIVE, 2.1, "2.0", False),
        (constants.NOT_EQUAL, "bar", "baz", True),
        (constants.NOT_EQUAL, "bar", "bar", False),
        (constants.NOT_EQUAL, 1, "2", True),
        (constants.NOT_EQUAL, 1, "1", False),
        (constants.NOT_EQUAL, True, "False", True),
        (constants.NOT_EQUAL, False, "True", True),
        (constants.NOT_EQUAL, False, "False", False),
        (constants.NOT_EQUAL, True, "True", False),
        (constants.CONTAINS, "bar", "b", True),
        (constants.CONTAINS, "bar", "bar", True),
        (constants.CONTAINS, "bar", "baz", False),
        (constants.NOT_CONTAINS, "bar", "b", False),
        (constants.NOT_CONTAINS, "bar", "bar", False),
        (constants.NOT_CONTAINS, "bar", "baz", True),
        (constants.REGEX, "foo", r"[a-z]+", True),
        (constants.REGEX, "FOO", r"[a-z]+", False),
        (constants.REGEX, "1.2.3", r"\d", True),
    ),
)
def test_segment_condition_matches_trait_value(
    operator, trait_value, condition_value, expected_result
):
    assert (
        SegmentConditionModel(
            operator=operator, property_="foo", value=condition_value
        ).matches_trait_value(
            trait_value=FlagsmithValue.from_untyped_value(trait_value)
        )
        == expected_result
    )


@pytest.mark.parametrize(
    "operator, trait_value, condition_value, expected_result",
    [
        (constants.EQUAL, "1.0.0", "1.0.0:semver", True),
        (constants.EQUAL, "1.0.0", "1.0.1:semver", False),
        (constants.NOT_EQUAL, "1.0.0", "1.0.0:semver", False),
        (constants.NOT_EQUAL, "1.0.0", "1.0.1:semver", True),
        (constants.GREATER_THAN, "1.0.1", "1.0.0:semver", True),
        (constants.GREATER_THAN, "1.0.0", "1.0.0-beta:semver", True),
        (constants.GREATER_THAN, "1.0.1", "1.2.0:semver", False),
        (constants.GREATER_THAN, "1.0.1", "1.0.1:semver", False),
        (constants.GREATER_THAN, "1.2.4", "1.2.3-pre.2+build.4:semver", True),
        (constants.LESS_THAN, "1.0.0", "1.0.1:semver", True),
        (constants.LESS_THAN, "1.0.0", "1.0.0:semver", False),
        (constants.LESS_THAN, "1.0.1", "1.0.0:semver", False),
        (constants.LESS_THAN, "1.0.0-rc.2", "1.0.0-rc.3:semver", True),
        (constants.GREATER_THAN_INCLUSIVE, "1.0.1", "1.0.0:semver", True),
        (constants.GREATER_THAN_INCLUSIVE, "1.0.1", "1.2.0:semver", False),
        (constants.GREATER_THAN_INCLUSIVE, "1.0.1", "1.0.1:semver", True),
        (constants.LESS_THAN_INCLUSIVE, "1.0.0", "1.0.1:semver", True),
        (constants.LESS_THAN_INCLUSIVE, "1.0.0", "1.0.0:semver", True),
        (constants.LESS_THAN_INCLUSIVE, "1.0.1", "1.0.0:semver", False),
    ],
)
def test_segment_condition_matches_trait_value_for_semver(
    identity, operator, trait_value, condition_value, expected_result
):
    assert (
        SegmentConditionModel(
            operator=operator, property_="version", value=condition_value
        ).matches_trait_value(trait_value=FlagsmithValue(value=trait_value))
        is expected_result
    )


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
def test_segment_rule_none(iterable, expected_result):
    assert SegmentRuleModel.none(iterable) is expected_result


@pytest.mark.parametrize(
    "rule_type, expected_function",
    (
        (constants.ALL_RULE, all),
        (constants.ANY_RULE, any),
        (constants.NONE_RULE, SegmentRuleModel.none),
    ),
)
def test_segment_rule_matching_function(rule_type, expected_function):
    assert SegmentRuleModel(type=rule_type).matching_function == expected_function
