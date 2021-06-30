import pytest

from flag_engine.environments.models import Environment
from flag_engine.features.models import Feature, FeatureState
from flag_engine.identities.models import Identity, Trait
from flag_engine.projects.models import Project
from flag_engine.segments import constants
from flag_engine.segments.models import Segment, SegmentCondition, SegmentRule

segment_condition_property = "foo"
segment_condition_string_value = "bar"


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
            FeatureState(feature=feature_1, enabled=True),
            FeatureState(feature=feature_2, enabled=False),
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
