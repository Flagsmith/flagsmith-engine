from unittest import mock

import pytest


# Some mock fixtures
from flag_engine.models import Project, Feature, FeatureState, Environment


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
def environment(feature_1, feature_2):
    return Environment(
        id=1,
        api_key="api-key",
        project=project,
        feature_states=[
            FeatureState(feature=feature_1, enabled=True),
            FeatureState(feature=feature_2, enabled=False),
        ],
    )
