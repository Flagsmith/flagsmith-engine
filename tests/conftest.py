from unittest import mock

import pytest


@pytest.fixture()
def mock_project():
    mock_project = mock.MagicMock(id=1)
    mock_project.name = "Test Project"  # `name` has meaning on mock init
    return mock_project


@pytest.fixture()
def mock_enabled_feature_state(mock_project):
    mock_feature = mock.MagicMock(id=1, project=mock_project)
    mock_feature.name = "enabled_feature"
    return mock.MagicMock(id=1, feature=mock_feature, enabled=True)


@pytest.fixture()
def mock_disabled_feature_state(mock_project):
    mock_feature = mock.MagicMock(id=1, project=mock_project)
    mock_feature.name = "disabled_feature"
    return mock.MagicMock(id=1, feature=mock_feature, enabled=False)
