import pytest

from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.segments.constants import (
    ALL_RULE,
    IS_NOT_SET,
    IS_SET,
    PERCENTAGE_SPLIT,
)
from flag_engine.segments.evaluator import evaluate_identity_in_segment
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from tests.unit.conftest import (
    segment_condition_property,
    segment_condition_string_value,
)

from .fixtures import (
    empty_segment,
    segment_conditions_and_nested_rules,
    segment_multiple_conditions_all,
    segment_multiple_conditions_any,
    segment_nested_rules,
    segment_single_condition,
    trait_key_1,
    trait_key_2,
    trait_key_3,
    trait_value_1,
    trait_value_2,
    trait_value_3,
)


@pytest.mark.parametrize(
    "segment, identity_traits, expected_result",
    (
        (empty_segment, [], False),
        (segment_single_condition, [], False),
        (
            segment_single_condition,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            True,
        ),
        (segment_multiple_conditions_all, [], False),
        (
            segment_multiple_conditions_all,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            False,
        ),
        (
            segment_multiple_conditions_all,
            [
                TraitModel(trait_key=trait_key_1, trait_value=trait_value_1),
                TraitModel(trait_key=trait_key_2, trait_value=trait_value_2),
            ],
            True,
        ),
        (segment_multiple_conditions_any, [], False),
        (
            segment_multiple_conditions_any,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            True,
        ),
        (
            segment_multiple_conditions_any,
            [TraitModel(trait_key=trait_key_2, trait_value=trait_value_2)],
            True,
        ),
        (
            segment_multiple_conditions_any,
            [
                TraitModel(trait_key=trait_key_1, trait_value=trait_value_1),
                TraitModel(trait_key=trait_key_2, trait_value=trait_value_2),
            ],
            True,
        ),
        (segment_nested_rules, [], False),
        (
            segment_nested_rules,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            False,
        ),
        (
            segment_nested_rules,
            [
                TraitModel(trait_key=trait_key_1, trait_value=trait_value_1),
                TraitModel(trait_key=trait_key_2, trait_value=trait_value_2),
                TraitModel(trait_key=trait_key_3, trait_value=trait_value_3),
            ],
            True,
        ),
        (segment_conditions_and_nested_rules, [], False),
        (
            segment_conditions_and_nested_rules,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            False,
        ),
        (
            segment_conditions_and_nested_rules,
            [
                TraitModel(trait_key=trait_key_1, trait_value=trait_value_1),
                TraitModel(trait_key=trait_key_2, trait_value=trait_value_2),
                TraitModel(trait_key=trait_key_3, trait_value=trait_value_3),
            ],
            True,
        ),
    ),
)
def test_identity_in_segment(segment, identity_traits, expected_result):
    identity = IdentityModel(
        identifier="foo",
        identity_traits=identity_traits,
        environment_api_key="api-key",
    )

    assert evaluate_identity_in_segment(identity, segment) == expected_result


@pytest.mark.parametrize(
    "segment_split_value, identity_hashed_percentage, expected_result",
    ((10, 1, True), (100, 50, True), (0, 1, False), (10, 20, False)),
)
def test_identity_in_segment_percentage_split(
    mocker, identity, segment_split_value, identity_hashed_percentage, expected_result
):
    # Given
    percentage_split_condition = SegmentConditionModel(
        operator=PERCENTAGE_SPLIT, value=str(segment_split_value)
    )
    rule = SegmentRuleModel(type=ALL_RULE, conditions=[percentage_split_condition])
    segment = SegmentModel(id=1, name="% split", rules=[rule])

    mock_get_hashed_percentage = mocker.patch(
        "flag_engine.segments.evaluator.get_hashed_percentage_for_object_ids"
    )
    mock_get_hashed_percentage.return_value = identity_hashed_percentage

    # When
    result = evaluate_identity_in_segment(identity=identity, segment=segment)

    # Then
    assert result == expected_result


@pytest.mark.parametrize(
    "operator, value, property_, expected_result",
    (
        (IS_SET, segment_condition_string_value, segment_condition_property, True),
        (IS_NOT_SET, segment_condition_string_value, segment_condition_property, False),
        (IS_SET, segment_condition_string_value, "random_property", False),
        (IS_NOT_SET, segment_condition_string_value, "random_property", True),
    ),
)
def test_identity_in_segment_is_set(
    mocker, identity_in_segment, operator, value, property_, expected_result
):
    # Given
    segment_condition_model = SegmentConditionModel(
        operator=operator,
        value=value,
        property_=property_,
    )
    rule = SegmentRuleModel(type=ALL_RULE, conditions=[segment_condition_model])
    segment = SegmentModel(id=1, name="segment model", rules=[rule])

    # When
    result = evaluate_identity_in_segment(identity=identity_in_segment, segment=segment)

    # Then
    assert result is expected_result
