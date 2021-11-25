import copy
from datetime import datetime

import pytest

from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.constants import MULTIVARIATE, STANDARD
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.models import IdentityModel, TraitModel
from flag_engine.organisations.models import OrganisationModel
from flag_engine.projects.models import ProjectModel
from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)

from .mock_django_classes import (
    DjangoEnvironment,
    DjangoFeature,
    DjangoFeatureSegment,
    DjangoFeatureState,
    DjangoMultivariateFeatureOption,
    DjangoMultivariateFeatureStateValue,
    DjangoOrganisation,
    DjangoProject,
    DjangoSegment,
    DjangoSegmentCondition,
    DjangoSegmentRule,
    DjangoTrait,
)

segment_condition_property = "foo"
segment_condition_string_value = "bar"


@pytest.fixture()
def django_organisation():
    return DjangoOrganisation(id=1, name="Test Org")


@pytest.fixture()
def django_project(django_organisation):
    return DjangoProject(id=1, name="Test Project", organisation=django_organisation)


@pytest.fixture()
def django_enabled_feature_state(django_project):
    feature = DjangoFeature(
        id=1, project=django_project, name="enabled_feature", type=STANDARD
    )
    return DjangoFeatureState(id=1, feature=feature, enabled=True)


@pytest.fixture()
def django_disabled_feature_state(django_project):
    feature = DjangoFeature(
        id=2, project=django_project, name="disabled_feature", type=STANDARD
    )
    return DjangoFeatureState(id=2, feature=feature, enabled=False)


@pytest.fixture()
def django_feature_with_string_value(django_project):
    return DjangoFeature(
        id=3,
        project=django_project,
        name="enabled_feature_with_string_value",
        type=STANDARD,
    )


@pytest.fixture()
def django_enabled_feature_state_with_string_value(django_feature_with_string_value):
    return DjangoFeatureState(
        id=3, feature=django_feature_with_string_value, enabled=True, value="foo"
    )


@pytest.fixture()
def django_multivariate_feature_state(django_project):
    feature = DjangoFeature(
        id=4, project=django_project, name="multivariate_feature", type=MULTIVARIATE
    )
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
def django_feature_segment(django_disabled_feature_state):
    feature_state = copy.deepcopy(django_disabled_feature_state)
    feature_state.id += 1
    feature_state.enabled = True
    return DjangoFeatureSegment(id=1, feature_states=[feature_state])


@pytest.fixture()
def django_segment(django_segment_rule, django_feature_segment):
    return DjangoSegment(
        id=1,
        name="segment",
        rules=[django_segment_rule],
        feature_segments=[django_feature_segment],
    )


@pytest.fixture()
def segment_condition():
    return SegmentConditionModel(
        operator=constants.EQUAL,
        property_=segment_condition_property,
        value=segment_condition_string_value,
    )


@pytest.fixture()
def segment_rule(segment_condition):
    return SegmentRuleModel(type=constants.ALL_RULE, conditions=[segment_condition])


@pytest.fixture()
def segment(segment_rule):
    return SegmentModel(id=1, name="my_segment", rules=[segment_rule])


@pytest.fixture()
def organisation():
    return OrganisationModel(
        id=1,
        name="test Org",
        stop_serving_flags=False,
        persist_trait_data=True,
        feature_analytics=True,
    )


@pytest.fixture()
def project(organisation, segment):
    return ProjectModel(
        id=1,
        name="Test Project",
        organisation=organisation,
        hide_disabled_flags=False,
        segments=[segment],
    )


@pytest.fixture()
def feature_1():
    return FeatureModel(id=1, name="feature_1", type=STANDARD)


@pytest.fixture()
def feature_2():
    return FeatureModel(id=2, name="feature_2", type=STANDARD)


@pytest.fixture()
def environment(feature_1, feature_2, project):
    return EnvironmentModel(
        id=1,
        api_key="api-key",
        project=project,
        feature_states=[
            FeatureStateModel(id=1, feature=feature_1, enabled=True),
            FeatureStateModel(id=2, feature=feature_2, enabled=False),
        ],
    )


@pytest.fixture()
def identity(environment):
    return IdentityModel(
        identifier="identity_1",
        environment_api_key=environment.api_key,
        created_date=datetime.now(),
    )


@pytest.fixture()
def trait_matching_segment(segment_condition):
    return TraitModel(
        trait_key=segment_condition.property_, trait_value=segment_condition.value
    )


@pytest.fixture()
def identity_in_segment(trait_matching_segment, environment):
    return IdentityModel(
        identifier="identity_2",
        environment_api_key=environment.api_key,
        identity_traits=[trait_matching_segment],
    )


@pytest.fixture()
def segment_override_fs(segment, feature_1):
    fs = FeatureStateModel(
        id=4,
        feature=feature_1,
        enabled=False,
    )
    fs.set_value("segment_override")
    return fs


@pytest.fixture()
def environment_with_segment_override(environment, segment_override_fs, segment):
    segment.feature_states.append(segment_override_fs)
    environment.project.segments.append(segment)
    return environment
