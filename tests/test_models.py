from flag_engine import constants
from flag_engine.constants import EQUAL
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
        name="my_segment",
        rules=[
            SegmentRule(
                type=constants.ALL_RULE,
                conditions=[
                    SegmentCondition(
                        operator=constants.EQUAL, property=trait_key, value=trait_value
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
