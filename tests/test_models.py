import pytest

from flag_engine import constants
from flag_engine.models import (
    Identity,
    FeatureState,
    Feature,
    Segment,
    SegmentRule,
    SegmentCondition,
    Trait,
    SegmentOverride,
)


def test_identity_get_all_feature_states_no_segments(feature_1, feature_2, environment):
    # Given
    overridden_feature = Feature(id=3, name="overridden_feature")

    # set the state of the feature to False in the environment configuration
    environment.feature_states.append(
        FeatureState(feature=overridden_feature, enabled=False)
    )

    # but True for the identity
    identity = Identity(
        id=1,
        identifier="identity",
        environment_id=environment.id,
        feature_states=[FeatureState(feature=overridden_feature, enabled=True)],
    )

    # When
    all_feature_states = identity.get_all_feature_states(environment=environment)

    # Then
    assert len(all_feature_states) == 3
    for feature_state in all_feature_states:
        environment_feature_state = environment.get_feature_state_for_feature(
            feature_state.feature
        )

        expected = (
            True
            if feature_state.feature == overridden_feature
            else environment_feature_state.enabled
        )
        assert feature_state.enabled is expected


def test_identity_get_all_feature_states_segments_only(
    feature_1, feature_2, environment
):
    # Given
    overridden_feature = Feature(id=3, name="overridden_feature")

    # set the state of the feature to False in the environment configuration
    environment.feature_states.append(
        FeatureState(feature=overridden_feature, enabled=False)
    )

    trait_key = "my_trait"
    trait_value = "my_value"

    segment = Segment(
        id=1,
        name="my_segment",
        rules=[
            SegmentRule(
                type=constants.ALL_RULE,
                conditions=[
                    SegmentCondition(
                        operator=constants.EQUAL, property_=trait_key, value=trait_value
                    )
                ],
            )
        ],
    )

    identity = Identity(
        id=1,
        identifier="identity",
        environment_id=environment.id,
        feature_states=[],
        traits=[Trait(trait_key=trait_key, trait_value=trait_value)],
    )

    environment.segment_overrides.append(
        SegmentOverride(
            segment=segment,
            feature_state=FeatureState(feature=overridden_feature, enabled=True),
        )
    )

    # When
    all_feature_states = identity.get_all_feature_states(environment=environment)

    # Then
    assert len(all_feature_states) == 3
    for feature_state in all_feature_states:
        environment_feature_state = environment.get_feature_state_for_feature(
            feature_state.feature
        )

        expected = (
            True
            if feature_state.feature == overridden_feature
            else environment_feature_state.enabled
        )
        assert feature_state.enabled is expected


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
