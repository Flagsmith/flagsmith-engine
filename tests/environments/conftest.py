import typing
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


@dataclass
class FeatureState:
    id: int
    feature: Feature
    enabled: bool
    _value: typing.Any = None

    def get_feature_state_value(self):
        return self._value


@pytest.fixture()
def mock_enabled_feature_state(mock_project):
    feature = Feature(id=1, project=mock_project, name="enabled_feature")
    return FeatureState(id=1, feature=feature, enabled=True)


@pytest.fixture()
def mock_disabled_feature_state(mock_project):
    feature = Feature(id=2, project=mock_project, name="disabled_feature")
    return FeatureState(id=2, feature=feature, enabled=False)


@pytest.fixture()
def enabled_feature_with_string_value(mock_project):
    return Feature(id=3, project=mock_project, name="enabled_feature_with_string_value")


@pytest.fixture()
def mock_enabled_feature_state_with_string_value(enabled_feature_with_string_value):
    return FeatureState(
        id=3, feature=enabled_feature_with_string_value, enabled=True, _value="foo"
    )
