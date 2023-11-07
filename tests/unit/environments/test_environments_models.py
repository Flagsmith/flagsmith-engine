from datetime import datetime, timedelta, timezone

import pytest

from flag_engine.environments.integrations.models import IntegrationModel
from flag_engine.environments.models import EnvironmentAPIKeyModel, EnvironmentModel


def test_environment_api_key_model_is_valid_is_true_for_non_expired_active_key() -> (
    None
):
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


def test_environment_api_key_model_is_valid_is_true_for_non_expired_active_key_with_expired_date_in_future() -> (
    None
):
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


def test_environment_api_key_model_is_valid_is_false_for_expired_active_key() -> None:
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


def test_environment_api_key_model_is_valid_is_false_for_non_expired_inactive_key() -> (
    None
):
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
    environment: EnvironmentModel,
) -> None:
    assert environment.integrations_data == {}


def test_environment_integrations_data_returns_correct_data_when_multiple_integrations(
    environment: EnvironmentModel,
) -> None:
    # Given
    example_key = "some-key"
    base_url = "https://some-integration-url"
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
    }


@pytest.mark.parametrize(
    "environment_value, project_value, expected_result",
    (
        (True, True, True),
        (True, False, True),
        (False, True, False),
        (False, False, False),
        (None, True, True),
        (None, False, False),
    ),
)
def test_environment_get_hide_disabled_flags(
    environment: EnvironmentModel,
    environment_value: bool,
    project_value: bool,
    expected_result: bool,
) -> None:
    # Given
    environment.hide_disabled_flags = environment_value
    environment.project.hide_disabled_flags = project_value

    # When
    result = environment.get_hide_disabled_flags()

    # Then
    assert result is expected_result
