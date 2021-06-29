from unittest import mock

import pytest

from flag_engine import constants
from flag_engine.models import (
    Project,
    Feature,
    FeatureState,
    Environment,
    Segment,
    SegmentRule,
    SegmentCondition,
    Trait, Identity,
)


segment_condition_property = "foo"
segment_condition_string_value = "bar"


@pytest.fixture()
def mock_project():
    mock_project = mock.MagicMock(id=1)
    mock_project.name = "Test Project"  # `name` has meaning on mock init
    return mock_project


@pytest.fixture()
def mock_feature_1(mock_project):
    mock_feature = mock.MagicMock(id=1, project=mock_project)
    mock_feature.name = "feature_1"
    return mock_feature


@pytest.fixture()
def mock_feature_2(mock_project):
    mock_feature = mock.MagicMock(id=2, project=mock_project)
    mock_feature.name = "feature_2"
    return mock_feature


@pytest.fixture()
def mock_enabled_feature_state(mock_feature_1):
    return mock.MagicMock(id=1, feature=mock_feature_1, enabled=True)


@pytest.fixture()
def mock_disabled_feature_state(mock_feature_2):
    return mock.MagicMock(id=1, feature=mock_feature_2, enabled=False)


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
        id=1,
        identifier="my-identifier",
        environment_id=environment.id,
        traits=[trait_matching_segment],
    )
