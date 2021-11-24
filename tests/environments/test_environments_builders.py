import json
from unittest import mock

from flag_engine.environments.builders import (
    build_environment_dict,
    build_environment_model,
)
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.constants import STANDARD
from flag_engine.features.models import (
    FeatureStateModel,
    MultivariateFeatureStateValueModel,
)
from flag_engine.utils.json.encoders import DecimalEncoder
from tests.helpers import (
    get_environment_feature_state_for_feature,
    get_environment_feature_state_for_feature_by_name,
)
from tests.mock_django_classes import DjangoEnvironment


def test_build_environment_dict(django_environment):
    # When
    environment_json = build_environment_dict(django_environment)

    # Then
    assert isinstance(environment_json, dict)
    assert json.dumps(environment_json, cls=DecimalEncoder)


def test_get_flags_for_environment_returns_feature_states_for_django_environment(
    django_environment,
    django_feature_with_string_value,
    django_enabled_feature_state_with_string_value,
):
    # Given
    # We convert the environment to a dictionary so we have a consistent input
    # between django and dynamo
    environment_dict = build_environment_dict(django_environment)

    # When
    # we build the environment model
    environment_model = build_environment_model(environment_dict)

    # Then
    # the returned object is an Environment object
    assert isinstance(environment_model, EnvironmentModel)

    # and each of the feature states are FeatureState objects
    assert len(environment_model.feature_states) == 4 and all(
        isinstance(feature_state, FeatureStateModel)
        for feature_state in environment_model.feature_states
    )

    # and the value is set correctly on the feature state which has a value
    assert (
        get_environment_feature_state_for_feature(
            environment=environment_model, feature=django_feature_with_string_value
        ).get_value()
        == django_enabled_feature_state_with_string_value.get_feature_state_value()
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
        "project": {
            "id": 1,
            "name": "test project",
            "organisation": {
                "id": 1,
                "name": "Test Org",
                "stop_serving_flags": False,
                "persist_trait_data": True,
                "feature_analytics": True,
            },
            "hide_disabled_flags": False,
        },
        "feature_states": [
            {
                "id": 1,
                "enabled": True,
                "value": None,
                "feature": {"id": 1, "name": "enabled_feature", "type": STANDARD},
            },
            {
                "id": 2,
                "enabled": False,
                "value": None,
                "feature": {"id": 2, "name": "disabled_feature", "type": STANDARD},
            },
            {
                "id": 3,
                "enabled": True,
                "value": string_value,
                "feature": {
                    "id": 3,
                    "name": feature_with_string_value_name,
                    "type": STANDARD,
                },
            },
        ],
    }

    # When
    # we build the environment model
    environment_model = build_environment_model(environment_dict)

    # Then
    # the returned object is an Environment object
    assert isinstance(environment_model, EnvironmentModel)

    # and each of the feature states are FeatureState objects
    assert len(environment_model.feature_states) == 3 and all(
        isinstance(feature_state, FeatureStateModel)
        for feature_state in environment_model.feature_states
    )

    # and the value is set correctly on the feature state which has a value
    assert (
        get_environment_feature_state_for_feature_by_name(
            environment_model, feature_with_string_value_name
        ).get_value()
        == string_value
    )


def test_build_environment_model_with_multivariate_flag(
    django_project, django_multivariate_feature_state
):
    # Given
    # a mock environment object to simulate a Django environment object
    django_environment = DjangoEnvironment(
        id=1, project=django_project, feature_states=[django_multivariate_feature_state]
    )
    environment_dict = build_environment_dict(django_environment)

    # When
    environment_model = build_environment_model(environment_dict)

    # Then
    assert isinstance(environment_model, EnvironmentModel)
    assert len(environment_model.feature_states) == 1

    fs = environment_model.feature_states[0]
    assert len(fs.multivariate_feature_state_values) == 2
    assert all(
        isinstance(mvfs, MultivariateFeatureStateValueModel)
        for mvfs in fs.multivariate_feature_state_values
    )


def test_environment_feature_states_are_filtered_correctly():
    # Given
    mock_feature_states = mock.MagicMock(spec=["filter"])
    mock_feature_states.filter.return_value = []

    mock_environment = mock.MagicMock(
        feature_states=mock_feature_states,
        spec=["id", "api_key", "feature_states", "project"],
    )
    environment_dict = build_environment_dict(mock_environment)

    # When
    build_environment_model(environment_dict)

    fs_call_without_segment_or_identity = mock.call(
        feature_segment_id=None, identity_id=None
    )
    fs_call_with_segment_overrides = mock.call(
        feature_segment_id__isnull=False, identity_id=None
    )
    # Then
    mock_feature_states.filter.assert_has_calls(
        [fs_call_without_segment_or_identity, fs_call_with_segment_overrides],
        any_order=True,
    )
