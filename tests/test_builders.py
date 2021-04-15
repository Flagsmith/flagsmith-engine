from unittest import mock

from flag_engine.builders import build_environment_model
from flag_engine.models import Environment, FeatureState


def test_get_flags_for_environment_returns_feature_states_for_django_environment(
    mock_project, mock_disabled_feature_state, mock_enabled_feature_state
):
    # Given
    # a mock environment object to simulate a Django environment object
    mock_fs_related_manager = mock.MagicMock()
    mock_fs_related_manager.all.return_value = [
        mock_disabled_feature_state,
        mock_enabled_feature_state,
    ]
    mock_environment = mock.MagicMock(
        id=1,
        api_key="api-key",
        project=mock_project,
        feature_states=mock_fs_related_manager,
    )
    mock_environment.name = "Test Environment"  # `name` has meaning on mock init

    # When
    # we build the environment model
    environment_model = build_environment_model(mock_environment)

    # Then
    # the returned object is an Environment object
    assert isinstance(environment_model, Environment)

    # and each of the feature states are FeatureState objects
    assert all(
        isinstance(feature_state, FeatureState)
        for feature_state in environment_model.feature_states
    )
