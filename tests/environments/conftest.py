import pytest

from .mock_django_classes import (
    DjangoFeature,
    DjangoFeatureState,
    DjangoMultivariateFeatureOption,
    DjangoMultivariateFeatureStateValue,
    DjangoProject,
)


@pytest.fixture()
def mock_project():
    return DjangoProject(1, "Test Project")


@pytest.fixture()
def mock_enabled_feature_state(mock_project):
    feature = DjangoFeature(id=1, project=mock_project, name="enabled_feature")
    return DjangoFeatureState(id=1, feature=feature, enabled=True)


@pytest.fixture()
def mock_disabled_feature_state(mock_project):
    feature = DjangoFeature(id=2, project=mock_project, name="disabled_feature")
    return DjangoFeatureState(id=2, feature=feature, enabled=False)


@pytest.fixture()
def enabled_feature_with_string_value(mock_project):
    return DjangoFeature(
        id=3, project=mock_project, name="enabled_feature_with_string_value"
    )


@pytest.fixture()
def mock_enabled_feature_state_with_string_value(enabled_feature_with_string_value):
    return DjangoFeatureState(
        id=3, feature=enabled_feature_with_string_value, enabled=True, value="foo"
    )


@pytest.fixture()
def mock_multivariate_feature_state(mock_project):
    feature = DjangoFeature(id=4, project=mock_project, name="multivariate_feature")
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
