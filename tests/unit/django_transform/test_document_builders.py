import json

from flag_engine.django_transform.document_builders import (
    build_environment_api_key_document,
    build_environment_document,
    build_identity_document,
)
from flag_engine.utils.json.encoders import DecimalEncoder


def test_build_identity_document(django_identity):
    # When
    identity_document = build_identity_document(django_identity)

    # Then
    assert (
        identity_document["composite_key"]
        == f"{django_identity.environment.api_key}_{django_identity.identifier}"
    )
    assert isinstance(identity_document, dict)
    assert json.dumps(identity_document, cls=DecimalEncoder)
    assert identity_document["django_id"] == django_identity.id
    assert identity_document["identity_uuid"] is not None


def test_build_environment_document(
    django_environment, django_project, django_segment, django_organisation
):
    # When
    environment_document = build_environment_document(django_environment)

    # Then
    assert environment_document["api_key"] == django_environment.api_key

    project = environment_document["project"]
    assert project["name"] == django_project.name
    assert len(project["segments"]) == 1
    assert project["hide_disabled_flags"] == django_project.hide_disabled_flags

    segment = project["segments"][0]
    assert segment["name"] == django_segment.name

    organisation = project["organisation"]
    assert organisation["name"] == django_organisation.name
    assert organisation["persist_trait_data"] == django_organisation.persist_trait_data
    assert organisation["stop_serving_flags"] == django_organisation.stop_serving_flags
    assert organisation["feature_analytics"] == django_organisation.feature_analytics

    assert len(environment_document["feature_states"]) == 4
    for feature_state in environment_document["feature_states"]:
        assert all(
            attr in feature_state
            for attr in (
                "feature_state_value",
                "multivariate_feature_state_values",
                "enabled",
                "django_id",
                "feature",
                "featurestate_uuid",
            )
        )


def test_build_environment_api_key_document(django_environment_api_key):
    # When
    api_key_document = build_environment_api_key_document(django_environment_api_key)

    # Then
    assert api_key_document["id"] == django_environment_api_key.id
    assert api_key_document["key"] == django_environment_api_key.key
    assert (
        api_key_document["client_api_key"]
        == django_environment_api_key.environment.api_key
    )
