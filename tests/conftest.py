import pytest

from flag_engine.environments.models import Environment
from flag_engine.features.models import Feature, FeatureState
from flag_engine.identities.models import Identity, Trait
from flag_engine.projects.models import Project
from flag_engine.segments import constants
from flag_engine.segments.models import Segment, SegmentCondition, SegmentRule

from .mock_django_classes import (
    DjangoEnvironment,
    DjangoFeature,
    DjangoFeatureState,
    DjangoMultivariateFeatureOption,
    DjangoMultivariateFeatureStateValue,
    DjangoProject,
)

segment_condition_property = "foo"
segment_condition_string_value = "bar"


@pytest.fixture()
def django_project():
    return DjangoProject(1, "Test Project")


@pytest.fixture()
def django_enabled_feature_state(django_project):
    feature = DjangoFeature(id=1, project=django_project, name="enabled_feature")
    return DjangoFeatureState(id=1, feature=feature, enabled=True)


@pytest.fixture()
def django_disabled_feature_state(django_project):
    feature = DjangoFeature(id=2, project=django_project, name="disabled_feature")
    return DjangoFeatureState(id=2, feature=feature, enabled=False)


@pytest.fixture()
def django_feature_with_string_value(django_project):
    return DjangoFeature(
        id=3, project=django_project, name="enabled_feature_with_string_value"
    )


@pytest.fixture()
def django_enabled_feature_state_with_string_value(django_feature_with_string_value):
    return DjangoFeatureState(
        id=3, feature=django_feature_with_string_value, enabled=True, value="foo"
    )


@pytest.fixture()
def django_multivariate_feature_state(django_project):
    feature = DjangoFeature(id=4, project=django_project, name="multivariate_feature")
    return DjangoFeatureState(
        id=4,
        feature=feature,
        enabled=True,
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


@pytest.fixture()
def django_environment(
    django_project,
    django_enabled_feature_state,
    django_disabled_feature_state,
    django_multivariate_feature_state,
    django_enabled_feature_state_with_string_value,
):
    return DjangoEnvironment(
        id=1,
        project=django_project,
        feature_states=[
            django_disabled_feature_state,
            django_enabled_feature_state,
            django_multivariate_feature_state,
            django_enabled_feature_state_with_string_value,
        ],
    )


@pytest.fixture()
def django_identity(django_environment):
    return Identity(
        id=1, identifier="test-identity", environment_id=django_environment.id
    )


@pytest.fixture()
def project():
    return Project(id=1, name="Test Project")


@pytest.fixture()
def feature_1():
    return Feature(id=1, name="feature_1")


@pytest.fixture()
def feature_2():
    return Feature(id=2, name="feature_2")


@pytest.fixture()
def environment(feature_1, feature_2, project):
    return Environment(
        id=1,
        api_key="api-key",
        project=project,
        feature_states=[
            FeatureState(id=1, feature=feature_1, enabled=True),
            FeatureState(id=2, feature=feature_2, enabled=False),
        ],
    )


@pytest.fixture()
def identity(environment):
    return Identity(id=1, identifier="identity_1", environment_id=environment.id)


@pytest.fixture()
def segment_condition():
    return SegmentCondition(
        operator=constants.EQUAL,
        property_=segment_condition_property,
        value=segment_condition_string_value,
    )


@pytest.fixture()
def segment_rule(segment_condition):
    return SegmentRule(type=constants.ALL_RULE, conditions=[segment_condition])


@pytest.fixture()
def segment(segment_rule):
    return Segment(id=1, name="my_segment", rules=[segment_rule])


@pytest.fixture()
def trait_matching_segment(segment_condition):
    return Trait(
        trait_key=segment_condition.property_, trait_value=segment_condition.value
    )


@pytest.fixture()
def identity_in_segment(trait_matching_segment, environment):
    return Identity(
        id=2,
        identifier="identity_2",
        environment_id=environment.id,
        traits=[trait_matching_segment],
    )
