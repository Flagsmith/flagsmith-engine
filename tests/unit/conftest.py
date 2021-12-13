from datetime import datetime

import pytest

from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.constants import STANDARD
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.organisations.models import OrganisationModel
from flag_engine.projects.models import ProjectModel
from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)

segment_condition_property = "foo"
segment_condition_string_value = "bar"


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
            FeatureStateModel(django_id=1, feature=feature_1, enabled=True),
            FeatureStateModel(django_id=2, feature=feature_2, enabled=False),
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
        django_id=4,
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
