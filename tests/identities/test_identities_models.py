import pytest

from flag_engine.features.models import Feature, FeatureState
from flag_engine.identities.models import Identity, Trait
from flag_engine.segments.models import SegmentOverride
from tests.helpers import get_environment_feature_state_for_feature
from tests.identities.fixtures import (
    empty_segment,
    segment_multiple_conditions_all,
    segment_multiple_conditions_any,
    segment_nested_rules_all,
    segment_nested_rules_any,
    segment_single_condition,
    trait_key_1,
    trait_key_2,
    trait_key_3,
    trait_value_1,
    trait_value_2,
    trait_value_3,
)


def test_identity_get_all_feature_states_no_segments(
    feature_1, feature_2, environment, identity
):
    # Given
    overridden_feature = Feature(id=3, name="overridden_feature")

    # set the state of the feature to False in the environment configuration
    environment.feature_states.append(
        FeatureState(id=3, feature=overridden_feature, enabled=False)
    )

    # but True for the identity
    identity.identity_features = [
        FeatureState(id=4, feature=overridden_feature, enabled=True)
    ]

    # When
    all_feature_states = identity.get_all_feature_states(environment=environment)

    # Then
    assert len(all_feature_states) == 3
    for feature_state in all_feature_states:
        environment_feature_state = get_environment_feature_state_for_feature(
            environment, feature_state.feature
        )

        expected = (
            True
            if feature_state.feature == overridden_feature
            else environment_feature_state.enabled
        )
        assert feature_state.enabled is expected


def test_identity_get_all_feature_states_segments_only(
    feature_1, feature_2, environment, segment, identity_in_segment
):
    # Given
    # a feature which we can override
    overridden_feature = Feature(id=3, name="overridden_feature")

    # which is given a default value of False in the environment configuration
    environment.feature_states.append(
        FeatureState(id=3, feature=overridden_feature, enabled=False)
    )

    # but overridden to True for identities in the segment
    environment.segment_overrides.append(
        SegmentOverride(
            segment=segment,
            feature_state=FeatureState(id=4, feature=overridden_feature, enabled=True),
        )
    )

    # When
    all_feature_states = identity_in_segment.get_all_feature_states(
        environment=environment
    )

    # Then
    assert len(all_feature_states) == 3
    for feature_state in all_feature_states:
        environment_feature_state = get_environment_feature_state_for_feature(
            environment, feature_state.feature
        )

        expected = (
            True
            if feature_state.feature == overridden_feature
            else environment_feature_state.enabled
        )
        assert feature_state.enabled is expected


@pytest.mark.parametrize(
    "segment, identity_traits, expected_in_segment",
    (
        (empty_segment, [], False),
        (segment_single_condition, [], False),
        (
            segment_single_condition,
            [Trait(trait_key=trait_key_1, trait_value=trait_value_1)],
            True,
        ),
        (segment_multiple_conditions_all, [], False),
        (
            segment_multiple_conditions_all,
            [Trait(trait_key=trait_key_1, trait_value=trait_value_1)],
            False,
        ),
        (
            segment_multiple_conditions_all,
            [
                Trait(trait_key=trait_key_1, trait_value=trait_value_1),
                Trait(trait_key=trait_key_2, trait_value=trait_value_2),
            ],
            True,
        ),
        (segment_multiple_conditions_any, [], False),
        (
            segment_multiple_conditions_any,
            [Trait(trait_key=trait_key_1, trait_value=trait_value_1)],
            True,
        ),
        (
            segment_multiple_conditions_any,
            [Trait(trait_key=trait_key_2, trait_value=trait_value_2)],
            True,
        ),
        (
            segment_multiple_conditions_any,
            [
                Trait(trait_key=trait_key_1, trait_value=trait_value_1),
                Trait(trait_key=trait_key_2, trait_value=trait_value_2),
            ],
            True,
        ),
        (segment_nested_rules_all, [], False),
        (
            segment_nested_rules_all,
            [Trait(trait_key=trait_key_1, trait_value=trait_value_1)],
            False,
        ),
        (
            segment_nested_rules_all,
            [
                Trait(trait_key=trait_key_1, trait_value=trait_value_1),
                Trait(trait_key=trait_key_2, trait_value=trait_value_2),
                Trait(trait_key=trait_key_3, trait_value=trait_value_3),
            ],
            True,
        ),
        (segment_nested_rules_any, [], False),
        (
            segment_nested_rules_any,
            [Trait(trait_key=trait_key_1, trait_value=trait_value_1)],
            False,
        ),
        (
            segment_nested_rules_any,
            [
                Trait(trait_key=trait_key_1, trait_value=trait_value_1),
                Trait(trait_key=trait_key_2, trait_value=trait_value_2),
            ],
            True,
        ),
        (
            segment_nested_rules_any,
            [Trait(trait_key=trait_key_3, trait_value=trait_value_3)],
            True,
        ),
    ),
)
def test_identity_in_segment(segment, identity_traits, expected_in_segment):
    assert (
        Identity(
            id=1, identifier="identity", environment_id=1, traits=identity_traits
        ).in_segment(segment)
        == expected_in_segment
    )
