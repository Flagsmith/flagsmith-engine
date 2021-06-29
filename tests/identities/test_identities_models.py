from flag_engine.features.models import Feature, FeatureState
from flag_engine.identities.models import Identity
from flag_engine.segments.models import SegmentOverride
from tests.identities.helpers import get_environment_feature_state_for_feature


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
        FeatureState(feature=overridden_feature, enabled=False)
    )

    # but overridden to True for identities in the segment
    environment.segment_overrides.append(
        SegmentOverride(
            segment=segment,
            feature_state=FeatureState(feature=overridden_feature, enabled=True),
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
