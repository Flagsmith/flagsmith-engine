from datetime import datetime, timedelta

from flag_engine.environments.models import EnvironmentAPIKeyModel


def test_environment_api_key_model_is_valid_is_true_for_non_expired_active_key():
    assert (
        EnvironmentAPIKeyModel(
            id=1,
            key="ser.random_key",
            name="test_key",
            created_at=datetime.now(),
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
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=5),
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
            created_at=datetime.now() - timedelta(days=5),
            expires_at=datetime.now(),
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
            created_at=datetime.now(),
            active=False,
            client_api_key="test_key",
        ).is_valid
        is False
    )
