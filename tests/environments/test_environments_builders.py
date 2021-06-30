from flag_engine.environments.builders import build_environment_model
from flag_engine.environments.models import Environment
from flag_engine.features.models import FeatureState
from tests.helpers import (
    get_environment_feature_state_for_feature,
    get_environment_feature_state_for_feature_by_name,
)


def test_get_flags_for_environment_returns_feature_states_for_django_environment(
    mock_project,
    mock_disabled_feature_state,
    mock_enabled_feature_state,
    mock_enabled_feature_state_with_string_value,
    enabled_feature_with_string_value,
):
    # Given
    # a mock environment object to simulate a Django environment object
    class MockEnvironment:
        class MockObjectManager:
            def all(self):
                return [
                    mock_disabled_feature_state,
                    mock_enabled_feature_state,
                    mock_enabled_feature_state_with_string_value,
                ]

        id = 1
        name = "Test Environment"
        api_key = "api-key"
        project = mock_project
        feature_states = MockObjectManager()

    # When
    # we build the environment model
    environment_model = build_environment_model(MockEnvironment())

    # Then
    # the returned object is an Environment object
    assert isinstance(environment_model, Environment)

    # and each of the feature states are FeatureState objects
    assert len(environment_model.feature_states) == 3 and all(
        isinstance(feature_state, FeatureState)
        for feature_state in environment_model.feature_states
    )

    # and the value is set correctly on the feature state which has a value
    assert (
        get_environment_feature_state_for_feature(
            environment=environment_model, feature=enabled_feature_with_string_value
        ).get_value()
        == mock_enabled_feature_state_with_string_value.get_feature_state_value()
    )


def test_get_flags_for_environment_returns_feature_states_for_environment_dictionary():
    # Given
    # some variables for use later
    string_value = "foo"
    feature_with_string_value_name = "feature_with_string_value"

    # and a dictionary to represent a Flagsmith environment
    environment_dict = {
        "id": 1,
        "api_key": "api-key",
        "project": {"id": 1, "name": "test project"},
        "feature_states": [
            {
                "id": 1,
                "enabled": True,
                "value": None,
                "feature": {"id": 1, "name": "enabled_feature"},
            },
            {
                "id": 2,
                "enabled": False,
                "value": None,
                "feature": {"id": 2, "name": "disabled_feature"},
            },
            {
                "id": 3,
                "enabled": True,
                "value": string_value,
                "feature": {"id": 3, "name": feature_with_string_value_name},
            },
        ],
    }

    # When
    # we build the environment model
    environment_model = build_environment_model(environment_dict)

    # Then
    # the returned object is an Environment object
    assert isinstance(environment_model, Environment)

    # and each of the feature states are FeatureState objects
    assert len(environment_model.feature_states) == 3 and all(
        isinstance(feature_state, FeatureState)
        for feature_state in environment_model.feature_states
    )

    # and the value is set correctly on the feature state which has a value
    assert (
        get_environment_feature_state_for_feature_by_name(
            environment_model, feature_with_string_value_name
        ).get_value()
        == string_value
    )
