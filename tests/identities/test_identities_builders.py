from flag_engine.identities.builders import build_identity_model
from flag_engine.identities.models import Identity
from tests.mock_django_classes import DjangoIdentity


def test_build_identity_model_no_feature_states(django_environment):
    # Given
    identity = DjangoIdentity(
        id=1, identifier="test-identity", environment=django_environment
    )

    # When
    identity_model = build_identity_model(identity)

    # Then
    assert isinstance(identity_model, Identity)
