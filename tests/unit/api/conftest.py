import copy
from datetime import datetime

import pytest

from flag_engine.features.constants import MULTIVARIATE, STANDARD
from flag_engine.segments import constants
from tests.mock_django_classes import (
    DjangoEnvironment,
    DjangoEnvironmentAPIKey,
    DjangoFeature,
    DjangoFeatureSegment,
    DjangoFeatureState,
    DjangoIdentity,
    DjangoMultivariateFeatureOption,
    DjangoMultivariateFeatureStateValue,
    DjangoOrganisation,
    DjangoProject,
    DjangoSegment,
    DjangoSegmentCondition,
    DjangoSegmentRule,
    DjangoTrait,
    DjangoWebhookConfig,
)


@pytest.fixture()
def django_organisation():
    return DjangoOrganisation(id=1, name="Test Org")


@pytest.fixture()
def django_project(django_organisation):
    return DjangoProject(id=1, name="Test Project", organisation=django_organisation)


@pytest.fixture()
def nested_environment(random_api_key, django_project, django_webhook):
    return DjangoEnvironment(
        id=1,
        api_key=random_api_key,
        project=django_project,
        webhook_config=django_webhook,
    )


@pytest.fixture()
def django_enabled_feature_state(django_project, nested_environment):
    feature = DjangoFeature(
        id=1, project=django_project, name="enabled_feature", type=STANDARD
    )
    return DjangoFeatureState(
        id=1, feature=feature, enabled=True, environment=nested_environment
    )


@pytest.fixture()
def django_disabled_feature_state(django_project, nested_environment):
    feature = DjangoFeature(
        id=2, project=django_project, name="disabled_feature", type=STANDARD
    )
    return DjangoFeatureState(
        id=2, feature=feature, enabled=False, environment=nested_environment
    )


@pytest.fixture()
def django_feature_with_string_value(django_project):
    return DjangoFeature(
        id=3,
        project=django_project,
        name="enabled_feature_with_string_value",
        type=STANDARD,
    )


@pytest.fixture()
def django_enabled_feature_state_with_string_value(
    django_feature_with_string_value, nested_environment
):
    return DjangoFeatureState(
        id=3,
        feature=django_feature_with_string_value,
        enabled=True,
        value="foo",
        environment=nested_environment,
    )


@pytest.fixture()
def django_multivariate_feature_state(django_project, nested_environment):
    feature = DjangoFeature(
        id=4, project=django_project, name="multivariate_feature", type=MULTIVARIATE
    )
    return DjangoFeatureState(
        id=4,
        feature=feature,
        enabled=True,
        environment=nested_environment,
        multivariate_feature_state_values=[
            DjangoMultivariateFeatureStateValue(
                id=1,
                percentage_allocation=30.0,
                multivariate_feature_option=DjangoMultivariateFeatureOption(
                    value="foo"
                ),
            ),
            DjangoMultivariateFeatureStateValue(
                id=2,
                percentage_allocation=30.0,
                multivariate_feature_option=DjangoMultivariateFeatureOption(value=123),
            ),
        ],
    )


@pytest.fixture
def django_webhook():
    return DjangoWebhookConfig(url="https://my.webhook.com/hook", secret="secret!")


@pytest.fixture()
def django_environment(
    django_project,
    django_enabled_feature_state,
    django_disabled_feature_state,
    django_multivariate_feature_state,
    django_enabled_feature_state_with_string_value,
    random_api_key,
    django_webhook,
):
    return DjangoEnvironment(
        id=1,
        api_key=random_api_key,
        project=django_project,
        feature_states=[
            django_disabled_feature_state,
            django_enabled_feature_state,
            django_multivariate_feature_state,
            django_enabled_feature_state_with_string_value,
        ],
        webhook_config=django_webhook,
    )


@pytest.fixture()
def django_environment_api_key(django_environment):
    return DjangoEnvironmentAPIKey(
        id=1,
        environment=django_environment,
        key="ser.random_key",
        created_at=datetime.now(),
        name="test_key",
    )


@pytest.fixture()
def django_trait_string():
    return DjangoTrait(trait_key="string_trait", trait_value="string_value")


@pytest.fixture()
def django_trait_integer():
    return DjangoTrait(trait_key="integer_trait", trait_value=10)


@pytest.fixture()
def django_trait_float():
    return DjangoTrait(trait_key="float_trait", trait_value=10.1)


@pytest.fixture()
def django_trait_boolean():
    return DjangoTrait(trait_key="boolean_trait", trait_value=True)


@pytest.fixture()
def django_segment_condition():
    return DjangoSegmentCondition(operator=constants.EQUAL, property="foo", value="bar")


@pytest.fixture()
def django_segment_rule(django_segment_condition):
    return DjangoSegmentRule(
        type=constants.ALL_RULE, conditions=[django_segment_condition]
    )


@pytest.fixture()
def django_feature_segment(mocker, django_disabled_feature_state, random_api_key):
    environment = mocker.MagicMock(api_key=random_api_key)
    feature_state = copy.deepcopy(django_disabled_feature_state)
    feature_state.id += 1
    feature_state.feature_segment = DjangoFeatureSegment(
        id_=1, priority=0, environment=environment
    )
    feature_state.enabled = True
    return DjangoFeatureSegment(
        id_=1,
        priority=0,
        environment=environment,
        feature_states=[feature_state],
    )


@pytest.fixture()
def django_segment(django_segment_rule, django_feature_segment, django_project):
    segment = DjangoSegment(
        id=1,
        name="segment",
        rules=[django_segment_rule],
        feature_segments=[django_feature_segment],
    )
    django_project.add_segment(segment)
    return segment


@pytest.fixture()
def django_identity(
    django_project,
    django_enabled_feature_state,
    django_enabled_feature_state_with_string_value,
    django_multivariate_feature_state,
    django_environment,
    django_trait_integer,
    django_trait_float,
    django_trait_string,
    django_trait_boolean,
):
    return DjangoIdentity(
        id=1,
        identifier="test-identity",
        created_date=datetime.now(),
        environment=django_environment,
        feature_states=[
            django_enabled_feature_state,
            django_enabled_feature_state_with_string_value,
            django_multivariate_feature_state,
        ],
        identity_traits=[
            django_trait_boolean,
            django_trait_float,
            django_trait_integer,
            django_trait_string,
        ],
    )
