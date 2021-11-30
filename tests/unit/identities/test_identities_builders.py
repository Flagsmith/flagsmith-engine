import json
from datetime import datetime

from flag_engine.features.constants import STANDARD
from flag_engine.features.models import FeatureStateModel
from flag_engine.identities.builders import build_identity_dict, build_identity_model
from flag_engine.identities.models import IdentityModel, TraitModel
from flag_engine.utils.json.encoders import DecimalEncoder
from tests.mock_django_classes import DjangoIdentity


def test_build_identity_dict(django_identity):
    # When
    identity_dict = build_identity_dict(django_identity)

    # Then
    assert (
        identity_dict["composite_key"]
        == f"{django_identity.environment.api_key}_{django_identity.identifier}"
    )
    assert isinstance(identity_dict, dict)
    assert json.dumps(identity_dict, cls=DecimalEncoder)
    assert identity_dict["django_id"] == django_identity.id
    assert identity_dict["identity_uuid"] is not None


def test_build_identity_model_from_django_no_feature_states(
    django_environment,
    django_trait_boolean,
    django_trait_float,
    django_trait_integer,
    django_trait_string,
):
    # Given
    django_identity = DjangoIdentity(
        id=1,
        identifier="test-identity",
        created_date=datetime.now(),
        environment=django_environment,
        identity_traits=[
            django_trait_string,
            django_trait_float,
            django_trait_integer,
            django_trait_boolean,
        ],
    )
    identity_dict = build_identity_dict(django_identity)

    # When
    identity_model = build_identity_model(identity_dict)

    # Then
    assert isinstance(identity_model, IdentityModel)
    assert len(identity_model.identity_features) == 0
    assert len(identity_model.identity_traits) == 4
    assert all(
        isinstance(trait, TraitModel) for trait in identity_model.identity_traits
    )


def test_build_identity_model_from_dictionary_no_feature_states(django_environment):
    # Given
    identity = {
        "id": 1,
        "identifier": "test-identity",
        "environment_api_key": django_environment.api_key,
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


def test_build_identity_model_from_django_with_feature_states(
    django_environment,
    django_enabled_feature_state,
    django_enabled_feature_state_with_string_value,
    django_multivariate_feature_state,
):
    # Given
    django_identity = DjangoIdentity(
        id=1,
        created_date=datetime.now(),
        identifier="test-identity",
        environment=django_environment,
        feature_states=[
            django_enabled_feature_state,
            django_enabled_feature_state_with_string_value,
            django_multivariate_feature_state,
        ],
    )
    identity_dict = build_identity_dict(django_identity)

    # When
    identity_model = build_identity_model(identity_dict)

    # Then
    assert isinstance(identity_model, IdentityModel)
    assert len(identity_model.identity_features) == 3
    assert all(
        isinstance(fs, FeatureStateModel) for fs in identity_model.identity_features
    )


def test_build_identity_model_from_dictionary_with_feature_states(
    django_environment,
    django_enabled_feature_state,
    django_enabled_feature_state_with_string_value,
    django_multivariate_feature_state,
):
    # Given
    identity_dict = {
        "id": 1,
        "identifier": "test-identity",
        "environment_api_key": django_environment.api_key,
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