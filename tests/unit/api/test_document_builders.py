import json
from datetime import timedelta

from flag_engine.api.document_builders import (
    build_environment_api_key_document,
    build_environment_document,
    build_identity_document,
)
from flag_engine.features.constants import STANDARD
from flag_engine.utils.datetime import utcnow_with_tz
from flag_engine.utils.json.encoders import DecimalEncoder
from tests.mock_django_classes import (
    DjangoEnvironment,
    DjangoFeature,
    DjangoFeatureState,
    DjangoIdentity,
)


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
    django_environment,
    django_project,
    django_segment,
    django_organisation,
    django_webhook,
    django_feature_segment,
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
    assert (
        segment["feature_states"][0]["feature_segment"]["priority"]
        == django_feature_segment.priority
    )
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

    assert environment_document["webhook_config"] is not None
    assert environment_document["webhook_config"]["url"] == django_webhook.url
    assert environment_document["webhook_config"]["secret"] == django_webhook.secret


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


def test_build_environment_document_with_multiple_feature_state_versions(
    django_project,
):
    # Given
    yesterday = utcnow_with_tz() - timedelta(days=1)
    tomorrow = utcnow_with_tz() + timedelta(days=1)

    # a feature
    feature = DjangoFeature(
        id=1, name="test_feature", project=django_project, type=STANDARD
    )

    # and 3 feature states for the same feature, 2 with live_from dates in the past and
    # one with a live from date in the future
    default_fs_kwargs = {"feature": feature, "live_from": yesterday, "enabled": True}
    feature_state_v1 = DjangoFeatureState(id=1, version=1, **default_fs_kwargs)
    feature_state_v2 = DjangoFeatureState(id=2, version=2, **default_fs_kwargs)
    feature_state_v3 = DjangoFeatureState(
        id=3, version=3, feature=feature, enabled=True, live_from=tomorrow
    )

    django_environment = DjangoEnvironment(
        id=1,
        project=django_project,
        feature_states=[feature_state_v1, feature_state_v2, feature_state_v3],
    )

    # When
    environment_document = build_environment_document(django_environment)

    # Then
    # we only get one feature state and it is the one that is the latest live version
    assert len(environment_document["feature_states"]) == 1
    assert environment_document["feature_states"][0]["django_id"] == feature_state_v2.id


def test_build_identity_document_with_multiple_feature_state_versions(
    django_environment, django_disabled_feature_state
):
    # Given
    yesterday = utcnow_with_tz() - timedelta(days=1)
    tomorrow = utcnow_with_tz() + timedelta(days=1)
    feature = django_disabled_feature_state.feature

    identity_feature_state_v1 = DjangoFeatureState(
        id=2, version=1, feature=feature, live_from=yesterday, enabled=True
    )
    identity_feature_state_v2 = DjangoFeatureState(
        id=3, version=2, feature=feature, live_from=yesterday, enabled=True
    )
    identity_feature_state_v3 = DjangoFeatureState(
        id=3, version=2, feature=feature, live_from=tomorrow, enabled=True
    )
    django_identity = DjangoIdentity(
        id=1,
        identifier="identity",
        created_date=yesterday,
        environment=django_environment,
        feature_states=[
            identity_feature_state_v1,
            identity_feature_state_v2,
            identity_feature_state_v3,
        ],
    )

    # When
    identity_document = build_identity_document(django_identity)

    # Then
    assert len(identity_document["identity_features"]) == 1
    assert (
        identity_document["identity_features"][0]["django_id"]
        == identity_feature_state_v2.id
    )
