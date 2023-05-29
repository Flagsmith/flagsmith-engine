import pytest

from flag_engine.engine import (
    get_environment_feature_state,
    get_environment_feature_states,
    get_identity_feature_state,
    get_identity_feature_states,
)
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.constants import STANDARD
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.utils.exceptions import FeatureStateNotFound
from tests.unit.helpers import get_environment_feature_state_for_feature


def test_identity_get_feature_state_without_any_override(
    environment, identity, feature_1
):
    # When
    feature_state = get_identity_feature_state(environment, identity, feature_1.name)
    # Then
    assert feature_state.feature == feature_1


def test_identity_get_feature_state__nonexistent_feature__raise_expected(
    environment: EnvironmentModel,
    identity: IdentityModel,
) -> None:
    # When & Then
    with pytest.raises(FeatureStateNotFound):
        get_identity_feature_state(environment, identity, "foobar")


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


@pytest.mark.parametrize(
    "environment_value, project_value, disabled_flag_returned",
    (
        (True, True, False),
        (True, False, False),
        (False, True, True),
        (False, False, True),
        (None, True, False),
        (None, False, True),
    ),
)
def test_get_identity_feature_states_hides_disabled_flags(
    environment,
    identity,
    feature_1,
    feature_2,
    environment_value,
    project_value,
    disabled_flag_returned,
):
    # Given - two identity overrides
    identity.identity_features = [
        FeatureStateModel(django_id=1, feature=feature_1, enabled=True),
        FeatureStateModel(django_id=2, feature=feature_2, enabled=False),
    ]

    environment.hide_disabled_flags = environment_value
    environment.project.hide_disabled_flags = project_value

    # When
    feature_states = get_identity_feature_states(
        environment=environment, identity=identity
    )

    # Then
    assert len(feature_states) == (2 if disabled_flag_returned else 1)


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
    environment_with_segment_override,
    identity_in_segment,
    identity,
    segment_condition_string_value,
    segment_condition_property,
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


def test_environment_get_all_feature_states(environment):
    # When
    feature_states = get_environment_feature_states(environment)

    # Then
    assert feature_states == environment.feature_states


@pytest.mark.parametrize(
    "environment_value, project_value, disabled_flag_returned",
    (
        (True, True, False),
        (True, False, False),
        (False, True, True),
        (False, False, True),
        (None, True, False),
        (None, False, True),
    ),
)
def test_environment_get_feature_states_hide_disabled_flags(
    environment, environment_value, project_value, disabled_flag_returned
):
    # Given
    environment.hide_disabled_flags = environment_value
    environment.project.hide_disabled_flags = project_value

    # When
    feature_states = get_environment_feature_states(environment)

    # Then
    assert len(feature_states) == (2 if disabled_flag_returned else 1)


def test_environment_get_feature_state(environment, feature_1):
    # When
    feature_state = get_environment_feature_state(environment, feature_1.name)

    # Then
    assert feature_state.feature == feature_1


def test_environment_get_feature_state_raises_feature_state_not_found(environment):
    with pytest.raises(FeatureStateNotFound):
        get_environment_feature_state(environment, "not_a_feature_name")
