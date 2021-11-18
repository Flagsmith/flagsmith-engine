from flag_engine.identities.models import IdentityModel


def test_composite_key():
    # Given
    environment_api_key = "abc123"
    identifier = "identity"
    identity_model = IdentityModel(
        environment_api_key=environment_api_key, identifier=identifier
    )

    # Then
    assert identity_model.composite_key == f"{environment_api_key}_{identifier}"


def test_generate_composite_key():
    # Given
    environment_api_key = "abc123"
    identifier = "identity"

    # Then
    assert (
        IdentityModel.generate_composite_key(
            env_key=environment_api_key, identifier=identifier
        )
        == f"{environment_api_key}_{identifier}"
    )
