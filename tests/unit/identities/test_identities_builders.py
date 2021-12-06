from flag_engine.features.constants import STANDARD
from flag_engine.features.models import FeatureStateModel
from flag_engine.identities.builders import build_identity_model
from flag_engine.identities.models import IdentityModel


def test_build_identity_model_from_dictionary_no_feature_states():
    # Given
    identity = {
        "id": 1,
        "identifier": "test-identity",
        "environment_api_key": "api-key",
        "created_date": "2021-08-22T06:25:23.406995Z",
        "identity_traits": [{"trait_key": "trait_key", "trait_value": "trait_value"}],
    }

    # When
    identity_model = build_identity_model(identity)

    # Then
    assert isinstance(identity_model, IdentityModel)
    assert len(identity_model.identity_features) == 0
    assert len(identity_model.identity_traits) == 1


def test_build_build_identity_model_from_dict_creates_identity_uuid():
    identity_model = build_identity_model(
        {"identifier": "test_user", "environment_api_key": "some_key"}
    )
    assert identity_model.identity_uuid is not None


def test_build_identity_model_from_dictionary_with_feature_states():
    # Given
    identity_dict = {
        "id": 1,
        "identifier": "test-identity",
        "environment_api_key": "api-key",
        "created_date": "2021-08-22T06:25:23.406995Z",
        "identity_features": [
            {
                "id": 1,
                "feature": {
                    "id": 1,
                    "name": "test_feature",
                    "type": STANDARD,
                },
                "enabled": True,
                "feature_state_value": "some-value",
            }
        ],
    }

    # When
    identity_model = build_identity_model(identity_dict)

    # Then
    assert isinstance(identity_model, IdentityModel)
    assert len(identity_model.identity_features) == 1
    assert isinstance(identity_model.identity_features[0], FeatureStateModel)
