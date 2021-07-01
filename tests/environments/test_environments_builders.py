from flag_engine.environments.builders import build_environment_model
from flag_engine.environments.models import Environment
from flag_engine.features.models import FeatureState, MultivariateFeatureStateValue
from tests.helpers import (
    get_environment_feature_state_for_feature,
    get_environment_feature_state_for_feature_by_name,
)
from tests.mock_django_classes import DjangoEnvironment


def test_get_flags_for_environment_returns_feature_states_for_django_environment(
    django_project,
    django_disabled_feature_state,
    django_enabled_feature_state,
    django_enabled_feature_state_with_string_value,
    django_feature_with_string_value,
):
    # Given
    # a mock environment object to simulate a Django environment object
    django_environment = DjangoEnvironment(
        id=1,
        project=django_project,
        feature_states=[
            django_disabled_feature_state,
            django_enabled_feature_state,
            django_enabled_feature_state_with_string_value,
        ],
    )

    # When
    # we build the environment model
    environment_model = build_environment_model(django_environment)

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


def test_build_environment_model_with_multivariate_flag(
    django_project, django_multivariate_feature_state
):
    # Given
    # a mock environment object to simulate a Django environment object
    django_environment = DjangoEnvironment(
        id=1, project=django_project, feature_states=[django_multivariate_feature_state]
    )

    # When
    environment_model = build_environment_model(django_environment)

    # Then
    assert isinstance(environment_model, Environment)
    assert len(environment_model.feature_states) == 1

    fs = environment_model.feature_states[0]
    assert len(fs.multivariate_feature_state_values) == 2
    assert all(
        isinstance(mvfs, MultivariateFeatureStateValue)
        for mvfs in fs.multivariate_feature_state_values
    )
