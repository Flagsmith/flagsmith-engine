import typing

import pytest
from pytest_lazyfixture import lazy_fixture
from pytest_mock import MockerFixture

from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.segments import constants
from flag_engine.segments.evaluator import (
    _matches_trait_value,
    evaluate_identity_in_segment,
)
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.segments.types import ConditionOperator
from tests.unit.segments.fixtures import (
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
def test_identity_in_segment(
    segment: SegmentModel,
    identity_traits: typing.List[TraitModel],
    expected_result: bool,
) -> None:
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
    mocker: MockerFixture,
    identity: IdentityModel,
    segment_split_value: int,
    identity_hashed_percentage: int,
    expected_result: bool,
) -> None:
    # Given
    percentage_split_condition = SegmentConditionModel(
        operator=constants.PERCENTAGE_SPLIT, value=str(segment_split_value)
    )
    rule = SegmentRuleModel(
        type=constants.ALL_RULE, conditions=[percentage_split_condition]
    )
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
    "operator,  property_, expected_result",
    (
        (constants.IS_SET, lazy_fixture("segment_condition_property"), True),
        (constants.IS_NOT_SET, lazy_fixture("segment_condition_property"), False),
        (constants.IS_SET, "random_property", False),
        (constants.IS_NOT_SET, "random_property", True),
    ),
)
def test_identity_in_segment_is_set_and_is_not_set(
    identity_in_segment: IdentityModel,
    operator: ConditionOperator,
    property_: str,
    expected_result: bool,
) -> None:
    # Given
    segment_condition_model = SegmentConditionModel(
        operator=operator,
        property_=property_,
    )
    rule = SegmentRuleModel(
        type=constants.ALL_RULE,
        conditions=[segment_condition_model],
    )
    segment = SegmentModel(id=1, name="segment model", rules=[rule])

    # When
    result = evaluate_identity_in_segment(identity=identity_in_segment, segment=segment)

    # Then
    assert result is expected_result


@pytest.mark.parametrize(
    "operator, trait_value, condition_value, expected_result",
    (
        (constants.EQUAL, "bar", "bar", True),
        (constants.EQUAL, "bar", "baz", False),
        (constants.EQUAL, 1, "1", True),
        (constants.EQUAL, 1, "not_an_int", False),
        (constants.EQUAL, 1, "2", False),
        (constants.EQUAL, True, "True", True),
        (constants.EQUAL, False, "False", True),
        (constants.EQUAL, False, "True", False),
        (constants.EQUAL, True, "False", False),
        (constants.EQUAL, 1.23, "1.23", True),
        (constants.EQUAL, 1.23, "not_a_float", False),
        (constants.EQUAL, 1.23, "4.56", False),
        (constants.EQUAL, 2, "not_an_number", False),
        (constants.GREATER_THAN, 2, "1", True),
        (constants.GREATER_THAN, 1, "1", False),
        (constants.GREATER_THAN, 0, "1", False),
        (constants.GREATER_THAN, 2.1, "2.0", True),
        (constants.GREATER_THAN, 2.1, "2.1", False),
        (constants.GREATER_THAN, 2.0, "2.1", False),
        (constants.GREATER_THAN, 2, "not_an_number", False),
        (constants.GREATER_THAN_INCLUSIVE, 2, "1", True),
        (constants.GREATER_THAN_INCLUSIVE, 1, "1", True),
        (constants.GREATER_THAN_INCLUSIVE, 0, "1", False),
        (constants.GREATER_THAN_INCLUSIVE, 2.1, "2.0", True),
        (constants.GREATER_THAN_INCLUSIVE, 2.1, "2.1", True),
        (constants.GREATER_THAN_INCLUSIVE, 2.0, "2.1", False),
        (constants.GREATER_THAN_INCLUSIVE, 2, "not_an_number", False),
        (constants.LESS_THAN, 1, "2", True),
        (constants.LESS_THAN, 1, "1", False),
        (constants.LESS_THAN, 1, "0", False),
        (constants.LESS_THAN, 2.0, "2.1", True),
        (constants.LESS_THAN, 2.1, "2.1", False),
        (constants.LESS_THAN, 2.1, "2.0", False),
        (constants.LESS_THAN, 2, "not_an_number", False),
        (constants.LESS_THAN_INCLUSIVE, 1, "2", True),
        (constants.LESS_THAN_INCLUSIVE, 1, "1", True),
        (constants.LESS_THAN_INCLUSIVE, 1, "0", False),
        (constants.LESS_THAN_INCLUSIVE, 2.0, "2.1", True),
        (constants.LESS_THAN_INCLUSIVE, 2.1, "2.1", True),
        (constants.LESS_THAN_INCLUSIVE, 2.1, "2.0", False),
        (constants.LESS_THAN_INCLUSIVE, 2, "not_a_number", False),
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
        (constants.CONTAINS, "bar", 1, False),
        (constants.NOT_CONTAINS, "bar", "b", False),
        (constants.NOT_CONTAINS, "bar", "bar", False),
        (constants.NOT_CONTAINS, "bar", "baz", True),
        (constants.REGEX, "foo", r"[a-z]+", True),
        (constants.REGEX, "FOO", r"[a-z]+", False),
        (constants.REGEX, "1.2.3", r"\d", True),
        (constants.REGEX, 1, r"\d", True),
        (constants.REGEX, None, r"[a-z]", False),
        (constants.REGEX, "foo", 12, False),
        (constants.IN, "foo", "", False),
        (constants.IN, "foo", "foo,bar", True),
        (constants.IN, "bar", "foo,bar", True),
        (constants.IN, "foo", "foo", True),
        (constants.IN, 1, "1,2,3,4", True),
        (constants.IN, 1, "", False),
        (constants.IN, 1, "1", True),
        (constants.IN, 1, None, False),
        (constants.IN, 1, None, False),
    ),
)
def test_segment_condition_matches_trait_value(
    operator: ConditionOperator,
    trait_value: typing.Union[None, int, str, float],
    condition_value: object,
    expected_result: bool,
) -> None:
    # Given
    segment_condition = SegmentConditionModel(
        operator=operator,
        property_="foo",
        value=condition_value,
    )

    # When
    result = _matches_trait_value(segment_condition, trait_value)

    # Then
    assert result == expected_result


def test_segment_condition__unsupported_operator__return_false(
    mocker: MockerFixture,
) -> None:
    # Given
    mocker.patch("flag_engine.segments.evaluator.MATCH_FUNCS_BY_OPERATOR", new={})
    segment_condition = SegmentConditionModel(
        operator=constants.EQUAL,
        property_="x",
        value="foo",
    )
    trait_value = "foo"

    # When
    result = _matches_trait_value(segment_condition, trait_value)

    # Then
    assert result is False


@pytest.mark.parametrize(
    "operator, trait_value, condition_value, expected_result",
    [
        (constants.EQUAL, "1.0.0", "1.0.0:semver", True),
        (constants.EQUAL, "not_a_semver", "1.0.0:semver", False),
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
    operator: ConditionOperator,
    trait_value: str,
    condition_value: str,
    expected_result: bool,
) -> None:
    # Given
    segment_condition = SegmentConditionModel(
        operator=operator,
        property_="version",
        value=condition_value,
    )

    # When
    result = _matches_trait_value(segment_condition, trait_value)

    # Then
    assert result == expected_result


@pytest.mark.parametrize(
    "trait_value, condition_value, expected_result",
    [
        (1, "2|0", False),
        (2, "2|0", True),
        (3, "2|0", False),
        (34.2, "4|3", False),
        (35.0, "4|3", True),
        ("dummy", "3|0", False),
        ("1.0.0", "3|0", False),
        (False, "1|3", False),
        (1, "invalid|value", False),
        (1, None, False),
    ],
)
def test_segment_condition_matches_trait_value_for_modulo(
    trait_value: typing.Union[int, float, str, bool],
    condition_value: typing.Optional[str],
    expected_result: bool,
) -> None:
    # Given
    segment_condition = SegmentConditionModel(
        operator=constants.MODULO,
        property_="version",
        value=condition_value,
    )

    # When
    result = _matches_trait_value(segment_condition, trait_value)

    # Then
    assert result == expected_result
