import typing

import pytest
from pytest_lazyfixture import lazy_fixture
from pytest_mock import MockerFixture

import flag_engine.segments.evaluator
from flag_engine.context.mappers import map_environment_identity_to_context
from flag_engine.context.types import (
    EvaluationContext,
    FeatureContext,
    SegmentCondition,
    SegmentContext,
)
from flag_engine.environments.models import EnvironmentModel
from flag_engine.identities.models import IdentityModel
from flag_engine.result.types import FlagResult
from flag_engine.segments import constants
from flag_engine.segments.evaluator import (
    _matches_context_value,
    context_matches_condition,
    get_context_segments,
    get_evaluation_result,
    get_flag_result_from_feature_context,
    get_identity_segments,
    is_context_in_segment,
)
from flag_engine.segments.models import SegmentModel
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
    "segment, context, expected_result",
    (
        (empty_segment, {"environment": {"key": "key", "name": "Environment"}}, False),
        (
            segment_single_condition,
            {"environment": {"key": "key", "name": "Environment"}},
            False,
        ),
        (
            segment_single_condition,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identity": {
                    "identifier": "foo",
                    "key": "key_foo",
                    "traits": {
                        trait_key_1: trait_value_1,
                    },
                },
            },
            True,
        ),
        (
            segment_multiple_conditions_all,
            {"environment": {"key": "key", "name": "Environment"}},
            False,
        ),
        (
            segment_multiple_conditions_all,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identity": {
                    "identifier": "foo",
                    "key": "key_foo",
                    "traits": {
                        trait_key_1: trait_value_1,
                    },
                },
            },
            False,
        ),
        (
            segment_multiple_conditions_all,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identity": {
                    "identifier": "foo",
                    "key": "key_foo",
                    "traits": {
                        trait_key_1: trait_value_1,
                        trait_key_2: trait_value_2,
                    },
                },
            },
            True,
        ),
        (
            segment_multiple_conditions_any,
            {"environment": {"key": "key", "name": "Environment"}},
            False,
        ),
        (
            segment_multiple_conditions_any,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identity": {
                    "identifier": "foo",
                    "key": "key_foo",
                    "traits": {
                        trait_key_1: trait_value_1,
                    },
                },
            },
            True,
        ),
        (
            segment_multiple_conditions_any,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identity": {
                    "identifier": "foo",
                    "key": "key_foo",
                    "traits": {
                        trait_key_2: trait_value_2,
                    },
                },
            },
            True,
        ),
        (
            segment_multiple_conditions_any,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identity": {
                    "identifier": "foo",
                    "key": "key_foo",
                    "traits": {
                        trait_key_1: trait_value_1,
                        trait_key_2: trait_value_2,
                    },
                },
            },
            True,
        ),
        (
            segment_nested_rules,
            {"environment": {"key": "key", "name": "Environment"}},
            False,
        ),
        (
            segment_nested_rules,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identity": {
                    "identifier": "foo",
                    "key": "key_foo",
                    "traits": {
                        trait_key_1: trait_value_1,
                    },
                },
            },
            False,
        ),
        (
            segment_nested_rules,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identifier": "foo",
                "key": "key_foo",
                "identity": {
                    "traits": {
                        trait_key_1: trait_value_1,
                        trait_key_2: trait_value_2,
                        trait_key_3: trait_value_3,
                    }
                },
            },
            True,
        ),
        (
            segment_conditions_and_nested_rules,
            {"environment": {"key": "key", "name": "Environment"}},
            False,
        ),
        (
            segment_conditions_and_nested_rules,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identifier": "foo",
                "key": "key_foo",
                "identity": {
                    "traits": {
                        trait_key_1: trait_value_1,
                    }
                },
            },
            False,
        ),
        (
            segment_conditions_and_nested_rules,
            {
                "environment": {"key": "key", "name": "Environment"},
                "identity": {
                    "identifier": "foo",
                    "key": "key_foo",
                    "traits": {
                        trait_key_1: trait_value_1,
                        trait_key_2: trait_value_2,
                        trait_key_3: trait_value_3,
                    },
                },
            },
            True,
        ),
    ),
)
def test_context_in_segment(
    segment: SegmentContext,
    context: EvaluationContext,
    expected_result: bool,
) -> None:
    assert is_context_in_segment(context, segment) == expected_result


@pytest.mark.parametrize(
    "segment_split_value, identity_hashed_percentage, expected_result",
    ((10, 1, True), (100, 50, True), (0, 1, False), (10, 20, False)),
)
def test_context_in_segment_percentage_split(
    mocker: MockerFixture,
    context: EvaluationContext,
    segment_split_value: int,
    identity_hashed_percentage: int,
    expected_result: bool,
) -> None:
    # Given
    segment_context = SegmentContext(
        key="1",
        name="% split",
        rules=[
            {
                "type": constants.ALL_RULE,
                "conditions": [],
                "rules": [
                    {
                        "type": constants.ALL_RULE,
                        "conditions": [
                            {
                                "operator": constants.PERCENTAGE_SPLIT,
                                "property": "",
                                "value": str(segment_split_value),
                            }
                        ],
                        "rules": [],
                    }
                ],
            }
        ],
    )

    mock_get_hashed_percentage = mocker.patch(
        "flag_engine.segments.evaluator.get_hashed_percentage_for_object_ids"
    )
    mock_get_hashed_percentage.return_value = identity_hashed_percentage

    # When
    result = is_context_in_segment(context=context, segment_context=segment_context)

    # Then
    assert result == expected_result


def test_get_identity_segments__calls__returns_expected(
    mocker: MockerFixture,
    environment: EnvironmentModel,
    identity_in_segment: IdentityModel,
) -> None:
    # Given
    get_evaluation_result_spy = mocker.spy(
        flag_engine.segments.evaluator, "get_evaluation_result"
    )
    expected_context = map_environment_identity_to_context(
        environment=environment,
        identity=identity_in_segment,
        override_traits=None,
    )

    # When
    result = get_identity_segments(identity_in_segment, environment)

    # Then
    get_evaluation_result_spy.assert_called_once_with(expected_context)
    assert result == [SegmentModel(id=1, name="my_segment")]


def test_get_context_segments__calls__returns_expected(
    mocker: MockerFixture,
    context_in_segment: EvaluationContext,
) -> None:
    # Given
    get_evaluation_result_spy = mocker.spy(
        flag_engine.segments.evaluator, "get_evaluation_result"
    )

    # When
    result = get_context_segments(context_in_segment)

    # Then
    get_evaluation_result_spy.assert_called_once_with(context_in_segment)
    assert result == [{"key": "1", "name": "my_segment"}]


def test_context_in_segment_percentage_split__trait_value__calls_expected(
    mocker: MockerFixture,
    context: EvaluationContext,
) -> None:
    # Given
    assert context["identity"] is not None
    context["identity"]["traits"]["custom_trait"] = "custom_value"

    segment_context = SegmentContext(
        key="1",
        name="% split",
        rules=[
            {
                "type": constants.ALL_RULE,
                "conditions": [],
                "rules": [
                    {
                        "type": constants.ALL_RULE,
                        "conditions": [
                            {
                                "operator": constants.PERCENTAGE_SPLIT,
                                "property": "custom_trait",
                                "value": "10",
                            }
                        ],
                        "rules": [],
                    }
                ],
            }
        ],
    )

    mock_get_hashed_percentage = mocker.patch(
        "flag_engine.segments.evaluator.get_hashed_percentage_for_object_ids"
    )
    mock_get_hashed_percentage.return_value = 1

    # When
    result = is_context_in_segment(context=context, segment_context=segment_context)

    # Then
    mock_get_hashed_percentage.assert_called_once_with(
        [segment_context["key"], "custom_value"]
    )
    assert result


@pytest.mark.parametrize(
    "operator,  property_, expected_result",
    (
        (constants.IS_SET, lazy_fixture("segment_condition_property"), True),
        (constants.IS_NOT_SET, lazy_fixture("segment_condition_property"), False),
        (constants.IS_SET, "random_property", False),
        (constants.IS_NOT_SET, "random_property", True),
    ),
)
def test_context_in_segment_is_set_and_is_not_set(
    context_in_segment: EvaluationContext,
    operator: ConditionOperator,
    property_: str,
    expected_result: bool,
) -> None:
    # Given
    segment_context: SegmentContext = {
        "key": "1",
        "name": "test_segment",
        "rules": [
            {
                "type": "ALL",
                "conditions": [
                    {
                        "property": property_,
                        "operator": operator,
                        "value": "",
                    }
                ],
            }
        ],
    }

    # When
    result = is_context_in_segment(context_in_segment, segment_context)

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
        (constants.CONTAINS, 1, "1", False),
        (constants.NOT_CONTAINS, "bar", "b", False),
        (constants.NOT_CONTAINS, "bar", "bar", False),
        (constants.NOT_CONTAINS, "bar", "baz", True),
        (constants.REGEX, "foo", r"[a-z]+", True),
        (constants.REGEX, "FOO", r"[a-z]+", False),
        (constants.REGEX, "1.2.3", r"\d", True),
        (constants.REGEX, 1, r"\d", True),
        (constants.REGEX, None, r"[a-z]", False),
        (constants.REGEX, "foo", 12, False),
        (constants.REGEX, 1, "1", True),
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
def test_segment_condition_matches_context_value(
    operator: ConditionOperator,
    trait_value: typing.Union[None, int, str, float],
    condition_value: str,
    expected_result: bool,
) -> None:
    # Given
    segment_condition: SegmentCondition = {
        "operator": operator,
        "property": "foo",
        "value": condition_value,
    }

    # When
    result = _matches_context_value(segment_condition, trait_value)

    # Then
    assert result == expected_result


def test_segment_condition__unsupported_operator__return_false(
    mocker: MockerFixture,
) -> None:
    # Given
    mocker.patch("flag_engine.segments.evaluator.MATCHERS_BY_OPERATOR", new={})
    segment_condition = SegmentCondition(
        operator=constants.EQUAL,
        property="x",
        value="foo",
    )
    trait_value = "foo"

    # When
    result = _matches_context_value(segment_condition, trait_value)

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
def test_segment_condition_matches_context_value_for_semver(
    operator: ConditionOperator,
    trait_value: str,
    condition_value: str,
    expected_result: bool,
) -> None:
    # Given
    segment_condition = SegmentCondition(
        operator=operator,
        property="version",
        value=condition_value,
    )

    # When
    result = _matches_context_value(segment_condition, trait_value)

    # Then
    assert result == expected_result


@pytest.mark.parametrize(
    "context,condition,segment_key,expected_result",
    (
        (
            {"identity": {"traits": {trait_key_1: False}}},
            SegmentCondition(
                operator=constants.EQUAL,
                property=trait_key_1,
                value="false",
            ),
            "segment_key",
            True,
        ),
        (
            {"identity": {"traits": {trait_key_1: True}}},
            SegmentCondition(
                operator=constants.EQUAL,
                property=trait_key_1,
                value="true",
            ),
            "segment_key",
            True,
        ),
        (
            {"identity": {"traits": {trait_key_1: 12}}},
            SegmentCondition(
                operator=constants.EQUAL,
                property=trait_key_1,
                value="12",
            ),
            "segment_key",
            True,
        ),
        (
            {"identity": {"traits": {trait_key_1: None}}},
            SegmentCondition(
                operator=constants.IS_SET,
                property=trait_key_1,
                value="false",
            ),
            "segment_key",
            False,
        ),
    ),
)
def test_context_matches_condition(
    context: EvaluationContext,
    condition: SegmentCondition,
    segment_key: str,
    expected_result: bool,
) -> None:
    # Given / When
    result = context_matches_condition(context, condition, segment_key)
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
        (1, "", False),
    ],
)
def test_segment_condition_matches_context_value_for_modulo(
    trait_value: typing.Union[int, float, str, bool],
    condition_value: str,
    expected_result: bool,
) -> None:
    # Given
    segment_condition = SegmentCondition(
        operator=constants.MODULO,
        property="version",
        value=condition_value,
    )

    # When
    result = _matches_context_value(segment_condition, trait_value)

    # Then
    assert result == expected_result


def test_get_evaluation_result__returns_expected(
    context_in_segment: EvaluationContext,
) -> None:
    # When
    result = get_evaluation_result(context_in_segment)

    # Then
    assert result == {
        "context": context_in_segment,
        "flags": [
            {
                "enabled": False,
                "feature_key": "1",
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=my_segment",
                "value": "segment_override",
            },
            {
                "enabled": False,
                "feature_key": "2",
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        ],
        "segments": [{"key": "1", "name": "my_segment"}],
    }


def test_get_evaluation_result__two_segments_override_same_feature__returns_expected() -> (
    None
):
    # Given
    context_in_segments: EvaluationContext = {
        "environment": {"key": "api-key", "name": ""},
        "identity": {
            "identifier": "identity_2",
            "key": "api-key_identity_2",
            "traits": {"foo": "bar"},
        },
        "features": {
            "feature_1": {
                "key": "1",
                "feature_key": "1",
                "name": "feature_1",
                "enabled": False,
                "value": None,
            },
            "feature_2": {
                "key": "2",
                "feature_key": "2",
                "name": "feature_2",
                "enabled": False,
                "value": None,
            },
        },
        "segments": {
            "1": {
                "key": "1",
                "name": "my_segment",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {"property": "foo", "operator": "EQUAL", "value": "bar"}
                        ],
                        "rules": [],
                    }
                ],
                "overrides": [
                    {
                        "key": "4",
                        "feature_key": "1",
                        "name": "feature_1",
                        "enabled": False,
                        "value": "segment_override",
                        "priority": 2,
                    }
                ],
            },
            "3": {
                "key": "3",
                "name": "higher_priority_segment",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {"property": "foo", "operator": "EQUAL", "value": "bar"}
                        ],
                        "rules": [],
                    }
                ],
                "overrides": [
                    {
                        "enabled": True,
                        "key": "2",
                        "feature_key": "1",
                        "name": "feature_1",
                        "value": "segment_override_other",
                        "priority": 1,
                    }
                ],
            },
        },
    }

    # When
    result = get_evaluation_result(context_in_segments)

    # Then
    assert result == {
        "context": context_in_segments,
        "flags": [
            {
                "enabled": True,
                "feature_key": "1",
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=higher_priority_segment",
                "value": "segment_override_other",
            },
            {
                "enabled": False,
                "feature_key": "2",
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        ],
        "segments": [
            {"key": "1", "name": "my_segment"},
            {"key": "3", "name": "higher_priority_segment"},
        ],
    }


@pytest.mark.parametrize(
    "percentage_value, expected_result",
    (
        (
            10,
            {
                "enabled": False,
                "feature_key": "1",
                "name": "my_feature",
                "reason": "SPLIT; weight=30",
                "value": "foo",
            },
        ),
        (
            40,
            {
                "enabled": False,
                "feature_key": "1",
                "name": "my_feature",
                "reason": "SPLIT; weight=30",
                "value": "bar",
            },
        ),
        (
            70,
            {
                "enabled": False,
                "feature_key": "1",
                "name": "my_feature",
                "reason": "DEFAULT",
                "value": "control",
            },
        ),
    ),
)
def test_get_flag_result_from_feature_context__call_return_expected(
    percentage_value: int,
    expected_result: FlagResult,
    mocker: MockerFixture,
) -> None:
    # Given
    expected_feature_context_key = "2"
    expected_key = "test_identifier"

    # we mock the function which gets the percentage value for an identity to
    # return a deterministic value so we know which value to expect
    get_hashed_percentage_for_object_ids_mock = mocker.patch(
        "flag_engine.segments.evaluator.get_hashed_percentage_for_object_ids",
    )
    get_hashed_percentage_for_object_ids_mock.return_value = percentage_value

    # and have a feature context with some multivariate feature options and associated values
    feature_context: FeatureContext = {
        "key": expected_feature_context_key,
        "feature_key": "1",
        "enabled": False,
        "name": "my_feature",
        "value": "control",
        "variants": [
            {"value": "foo", "weight": 30},
            {"value": "bar", "weight": 30},
        ],
    }

    # When
    result = get_flag_result_from_feature_context(
        feature_context=feature_context,
        key=expected_key,
    )

    # the value of the feature state is correct based on the percentage value returned
    assert result == expected_result

    # the function is called with the expected key
    get_hashed_percentage_for_object_ids_mock.assert_called_once_with(
        [
            expected_feature_context_key,
            expected_key,
        ]
    )
