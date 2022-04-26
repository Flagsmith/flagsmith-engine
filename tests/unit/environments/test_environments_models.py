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


def test_environment_has_integrations_false_when_no_integrations(
    environment,
):
    assert environment.has_integrations is False


def test_environment_has_integrations_true_when_integrations_exist(
    environment,
):
    # Given
    example_key = "some-key"
    segment_url = "https://api.segment.com"

    environment.mixpanel_config = IntegrationModel(api_key=example_key)
    environment.segment_config = IntegrationModel(
        api_key=example_key, base_url=segment_url
    )

    # Then
    assert environment.has_integrations is True
