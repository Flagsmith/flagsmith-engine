import pytest

from flag_engine.segments import constants
from flag_engine.segments.models import SegmentCondition


@pytest.mark.parametrize(
    "operator, trait_value, condition_value, expected_result",
    (
        (constants.EQUAL, "bar", "bar", True),
        (constants.EQUAL, "bar", "baz", False),
        (constants.EQUAL, 1, 1, True),
        (constants.EQUAL, 1, 2, False),
        (constants.EQUAL, True, True, True),
        (constants.EQUAL, False, False, True),
        (constants.EQUAL, False, True, False),
        (constants.EQUAL, True, False, False),
        (constants.EQUAL, 1.23, 1.23, True),
        (constants.EQUAL, 1.23, 4.56, False),
        (constants.GREATER_THAN, 2, 1, True),
        (constants.GREATER_THAN, 1, 1, False),
        (constants.GREATER_THAN, 0, 1, False),
        (constants.GREATER_THAN, 2.1, 2.0, True),
        (constants.GREATER_THAN, 2.1, 2.1, False),
        (constants.GREATER_THAN, 2.0, 2.1, False),
        (constants.GREATER_THAN_INCLUSIVE, 2, 1, True),
        (constants.GREATER_THAN_INCLUSIVE, 1, 1, True),
        (constants.GREATER_THAN_INCLUSIVE, 0, 1, False),
        (constants.GREATER_THAN_INCLUSIVE, 2.1, 2.0, True),
        (constants.GREATER_THAN_INCLUSIVE, 2.1, 2.1, True),
        (constants.GREATER_THAN_INCLUSIVE, 2.0, 2.1, False),
        (constants.LESS_THAN, 1, 2, True),
        (constants.LESS_THAN, 1, 1, False),
        (constants.LESS_THAN, 1, 0, False),
        (constants.LESS_THAN, 2.0, 2.1, True),
        (constants.LESS_THAN, 2.1, 2.1, False),
        (constants.LESS_THAN, 2.1, 2.0, False),
        (constants.LESS_THAN_INCLUSIVE, 1, 2, True),
        (constants.LESS_THAN_INCLUSIVE, 1, 1, True),
        (constants.LESS_THAN_INCLUSIVE, 1, 0, False),
        (constants.LESS_THAN_INCLUSIVE, 2.0, 2.1, True),
        (constants.LESS_THAN_INCLUSIVE, 2.1, 2.1, True),
        (constants.LESS_THAN_INCLUSIVE, 2.1, 2.0, False),
        (constants.NOT_EQUAL, "bar", "baz", True),
        (constants.NOT_EQUAL, "bar", "bar", False),
        (constants.NOT_EQUAL, 1, 2, True),
        (constants.NOT_EQUAL, 1, 1, False),
        (constants.NOT_EQUAL, True, False, True),
        (constants.NOT_EQUAL, False, True, True),
        (constants.NOT_EQUAL, False, False, False),
        (constants.NOT_EQUAL, True, True, False),
        (constants.CONTAINS, "bar", "b", True),
        (constants.CONTAINS, "bar", "bar", True),
        (constants.CONTAINS, "bar", "baz", False),
        (constants.NOT_CONTAINS, "bar", "b", False),
        (constants.NOT_CONTAINS, "bar", "bar", False),
        (constants.NOT_CONTAINS, "bar", "baz", True),
    ),
)
def test_segment_condition_matches_trait_value(
    operator, trait_value, condition_value, expected_result
):
    assert (
        SegmentCondition(
            operator=operator, property_="foo", value=condition_value
        ).matches_trait_value(trait_value=trait_value)
        == expected_result
    )
