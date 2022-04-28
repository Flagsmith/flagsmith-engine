from flag_engine.environments.builders import (
    build_environment_api_key_model,
    build_environment_model,
)
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.constants import STANDARD
from flag_engine.features.models import (
    FeatureStateModel,
    MultivariateFeatureStateValueModel,
)
from flag_engine.utils.models import FlagsmithValue
from tests.unit.helpers import get_environment_feature_state_for_feature_by_name


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
                "feature_state_value": None,
                "feature": {"id": 1, "name": "enabled_feature", "type": STANDARD},
            },
            {
                "id": 2,
                "enabled": False,
                "feature_state_value": None,
                "feature": {"id": 2, "name": "disabled_feature", "type": STANDARD},
            },
            {
                "id": 3,
                "enabled": True,
                "feature_state_value": string_value,
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
    assert get_environment_feature_state_for_feature_by_name(
        environment_model, feature_with_string_value_name
    ).get_value() == FlagsmithValue(value=string_value)


def test_build_environment_model_with_multivariate_flag():
    # Given
    variate_1_value = "value-1"
    variate_2_value = "value-2"
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
                "feature_state_value": None,
                "feature": {
                    "id": 1,
                    "name": "enabled_feature",
                    "type": STANDARD,
                },
                "multivariate_feature_state_values": [
                    {
                        "id": 1,
                        "percentage_allocation": 10.0,
                        "multivariate_feature_option": {
                            "value": variate_1_value,
                        },
                    },
                    {
                        "id": 2,
                        "percentage_allocation": 10.0,
                        "multivariate_feature_option": {
                            "value": variate_2_value,
                            "id": 2,
                        },
                    },
                ],
            },
        ],
    }

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


def test_build_environment_api_key_model():
    # Given
    environment_key_dict = {
        "key": "ser.7duQYrsasJXqdGsdaagyfU",
        "active": True,
        "created_at": "2022-02-07T04:58:25.969438+00:00",
        "client_api_key": "RQchaCQ2mYicSCAwKoAg2E",
        "id": 10,
        "name": "api key 2",
        "expires_at": None,
    }
    # When
    environment_key_model = build_environment_api_key_model(environment_key_dict)

    # Then
    assert environment_key_model.key == environment_key_dict["key"]
