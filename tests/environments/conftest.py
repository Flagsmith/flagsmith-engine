from dataclasses import dataclass

import pytest


@dataclass
class Project:
    id: int
    name: str


@pytest.fixture()
def mock_project():
    return Project(1, "Test Project")


@dataclass
class Feature:
    id: int
    name: str
    project: Project


@pytest.fixture()
def mock_feature_1(mock_project):
    return Feature(id=1, project=mock_project, name="feature_1")


@pytest.fixture()
def mock_feature_2(mock_project):
    return Feature(id=2, project=mock_project, name="feature_2")


@dataclass
class FeatureState:
    id: int
    feature: Feature
    enabled: bool


@pytest.fixture()
def mock_enabled_feature_state(mock_feature_1):
    return FeatureState(id=1, feature=mock_feature_1, enabled=True)


@pytest.fixture()
def mock_disabled_feature_state(mock_feature_2):
    return FeatureState(id=2, feature=mock_feature_2, enabled=False)
