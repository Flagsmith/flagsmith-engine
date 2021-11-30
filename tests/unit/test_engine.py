from flag_engine.engine import get_identity_flag, get_identity_flags
from flag_engine.features.constants import STANDARD
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.models import TraitModel
from tests.unit.conftest import (
    segment_condition_property,
    segment_condition_string_value,
)
from tests.unit.helpers import (
    get_environment_feature_state_for_feature,
    get_environment_flag_for_feature,
)


def test_identity_get_feature_state_without_any_override(
    environment, identity, feature_1
):
    # Given
    default_flag = get_environment_flag_for_feature(environment, feature_1)

    # When
    flag = get_identity_flag(environment, identity, feature_1.name)

    # Then
    assert flag.feature == feature_1
    assert flag.value == default_flag.value


def test_identity_get_all_feature_states_no_segments(
    feature_1, feature_2, environment, identity
):
    # Given
    overridden_feature = FeatureModel(id=3, name="overridden_feature", type=STANDARD)

    # set the state of the feature to False in the environment configuration
    environment.feature_states.append(
        FeatureStateModel(id=3, feature=overridden_feature, enabled=False)
    )

    # but True for the identity
    identity.identity_features = [
        FeatureStateModel(id=4, feature=overridden_feature, enabled=True)
    ]

    # When
    all_flags = get_identity_flags(environment=environment, identity=identity)

    # Then
    assert len(all_flags) == 3
    for flag in all_flags:
        environment_feature_state = get_environment_feature_state_for_feature(
            environment, flag.feature
        )

        expected = (
            True
            if flag.feature == overridden_feature
            else environment_feature_state.enabled
        )
        assert flag.enabled is expected


def test_identity_get_all_feature_states_segments_only(
    feature_1, feature_2, environment, segment, identity_in_segment
):
    # Given
    # a feature which we can override
    overridden_feature = FeatureModel(id=3, name="overridden_feature", type=STANDARD)

    # which is given a default value of False in the environment configuration
    environment.feature_states.append(
        FeatureStateModel(id=3, feature=overridden_feature, enabled=False)
    )

    # but overridden to True for identities in the segment
    segment.feature_states.append(
        FeatureStateModel(
            id=4, feature=overridden_feature, enabled=True, segment_id=segment.id
        )
    )

    # When
    all_flags = get_identity_flags(
        environment=environment, identity=identity_in_segment
    )

    # Then
    assert len(all_flags) == 3
    for flag in all_flags:
        environment_feature_state = get_environment_feature_state_for_feature(
            environment, flag.feature
        )

        expected = (
            True
            if flag.feature == overridden_feature
            else environment_feature_state.enabled
        )
        assert flag.enabled is expected


def test_identity_get_all_feature_states_with_traits(
    environment_with_segment_override, identity_in_segment, identity
):
    # Given
    trait_models = TraitModel(
        trait_key=segment_condition_property, trait_value=segment_condition_string_value
    )

    # When
    all_flags = get_identity_flags(
        environment=environment_with_segment_override,
        identity=identity_in_segment,
        override_traits=[trait_models],
    )

    # Then
    assert all_flags[0].value == "segment_override"
