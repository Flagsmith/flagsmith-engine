import pytest

from tests.mock_django_classes import DjangoIdentity


@pytest.fixture()
def django_identity(
    django_project,
    django_enabled_feature_state,
    django_enabled_feature_state_with_string_value,
    django_multivariate_feature_state,
    django_environment,
):
    return DjangoIdentity(
        id=1,
        identifier="test-identity",
        environment=django_environment,
        feature_states=[
            django_enabled_feature_state,
            django_enabled_feature_state_with_string_value,
            django_multivariate_feature_state,
        ],
    )
