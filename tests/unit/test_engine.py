from flag_engine.engine import get_identity_feature_state, get_identity_feature_states
from flag_engine.features.constants import STANDARD
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.traits.models import TraitModel
from tests.unit.conftest import (
    segment_condition_property,
    segment_condition_string_value,
)
from tests.unit.helpers import get_environment_feature_state_for_feature


def test_identity_get_feature_state_without_any_override(
    environment, identity, feature_1
):
    # When
    feature_state = get_identity_feature_state(environment, identity, feature_1.name)
    # Then
    assert feature_state.feature == feature_1


def test_identity_get_all_feature_states_no_segments(
    feature_1, feature_2, environment, identity
):
    # Given
    overridden_feature = FeatureModel(id=3, name="overridden_feature", type=STANDARD)

    # set the state of the feature to False in the environment configuration
    environment.feature_states.append(
        FeatureStateModel(django_id=3, feature=overridden_feature, enabled=False)
    )

    # but True for the identity
    identity.identity_features = [
        FeatureStateModel(django_id=4, feature=overridden_feature, enabled=True)
    ]

    # When
    all_feature_states = get_identity_feature_states(
        environment=environment, identity=identity
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


def test_identity_get_all_feature_states_segments_only(
    feature_1, feature_2, environment, segment, identity_in_segment
):
    # Given
    # a feature which we can override
    overridden_feature = FeatureModel(id=3, name="overridden_feature", type=STANDARD)

    # which is given a default value of False in the environment configuration
    environment.feature_states.append(
        FeatureStateModel(django_id=3, feature=overridden_feature, enabled=False)
    )

    # but overridden to True for identities in the segment
    segment.feature_states.append(
        FeatureStateModel(django_id=4, feature=overridden_feature, enabled=True)
    )

    # When
    all_feature_states = get_identity_feature_states(
        environment=environment, identity=identity_in_segment
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


def test_identity_get_all_feature_states_with_traits(
    environment_with_segment_override, identity_in_segment, identity
):
    # Given
    trait_models = TraitModel(
        trait_key=segment_condition_property, trait_value=segment_condition_string_value
    )

    # When
    all_feature_states = get_identity_feature_states(
        environment=environment_with_segment_override,
        identity=identity_in_segment,
        override_traits=[trait_models],
    )

    # Then
    assert all_feature_states[0].get_value() == "segment_override"
