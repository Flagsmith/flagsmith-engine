from flag_engine.environments.builders import build_environment_model
from flag_engine.environments.models import Environment
from flag_engine.features.models import FeatureState


def test_get_flags_for_environment_returns_feature_states_for_django_environment(
    mock_project, mock_disabled_feature_state, mock_enabled_feature_state
):
    # Given
    # a mock environment object to simulate a Django environment object
    class MockEnvironment:
        class MockObjectManager:
            def all(self):
                return [mock_disabled_feature_state, mock_enabled_feature_state]

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
    assert len(environment_model.feature_states) == 2 and all(
        isinstance(feature_state, FeatureState)
        for feature_state in environment_model.feature_states
    )


def test_get_flags_for_environment_returns_feature_states_for_environment_dictionary():
    # Given
    # a dictionary to represent a Flagsmith environment
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
        ],
    }

    # When
    # we build the environment model
    environment_model = build_environment_model(environment_dict)

    # Then
    # the returned object is an Environment object
    assert isinstance(environment_model, Environment)

    # and each of the feature states are FeatureState objects
    assert len(environment_model.feature_states) == 2 and all(
        isinstance(feature_state, FeatureState)
        for feature_state in environment_model.feature_states
    )
