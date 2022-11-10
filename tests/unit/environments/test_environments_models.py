from datetime import datetime, timedelta, timezone

from flag_engine.environments.integrations.models import IntegrationModel
from flag_engine.environments.models import EnvironmentAPIKeyModel


def test_environment_api_key_model_is_valid_is_true_for_non_expired_active_key():
    assert (
        EnvironmentAPIKeyModel(
            id=1,
            key="ser.random_key",
            name="test_key",
            created_at=datetime.now(tz=timezone.utc),
            client_api_key="test_key",
        ).is_valid
        is True
    )


def test_environment_api_key_model_is_valid_is_true_for_non_expired_active_key_with_expired_date_in_future():
    assert (
        EnvironmentAPIKeyModel(
            id=1,
            key="ser.random_key",
            name="test_key",
            created_at=datetime.now(tz=timezone.utc),
            expires_at=datetime.now(tz=timezone.utc) + timedelta(days=5),
            client_api_key="test_key",
        ).is_valid
        is True
    )


def test_environment_api_key_model_is_valid_is_false_for_expired_active_key():
    assert (
        EnvironmentAPIKeyModel(
            id=1,
            key="ser.random_key",
            name="test_key",
            created_at=datetime.now(tz=timezone.utc) - timedelta(days=5),
            expires_at=datetime.now(tz=timezone.utc),
            client_api_key="test_key",
        ).is_valid
        is False
    )


def test_environment_api_key_model_is_valid_is_false_for_non_expired_inactive_key():
    assert (
        EnvironmentAPIKeyModel(
            id=1,
            key="ser.random_key",
            name="test_key",
            created_at=datetime.now(tz=timezone.utc),
            active=False,
            client_api_key="test_key",
        ).is_valid
        is False
    )


def test_environment_integrations_data_returns_empty_dict_when_no_integrations(
    environment,
):
    assert environment.integrations_data == {}


def test_environment_integrations_data_returns_correct_data_when_multiple_integrations(
    environment,
):
    # Given
    example_key = "some-key"
    base_url = "https://some-integration-url"
    entity_selector = "some-entity-selector"
    environment.dynatrace_config = IntegrationModel(
        api_key=example_key,
        base_url=base_url,
        entity_selector=entity_selector,
    )
    environment.mixpanel_config = IntegrationModel(api_key=example_key)
    environment.segment_config = IntegrationModel(
        api_key=example_key, base_url=base_url
    )

    # When
    integrations_data = environment.integrations_data

    # Then
    assert integrations_data == {
        "mixpanel_config": {
            "api_key": example_key,
            "base_url": None,
            "entity_selector": None,
        },
        "segment_config": {
            "api_key": example_key,
            "base_url": base_url,
            "entity_selector": None,
        },
        "dynatrace_config": {
            "api_key": example_key,
            "base_url": base_url,
            "entity_selector": entity_selector,
        },
    }
