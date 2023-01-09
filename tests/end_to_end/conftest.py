import pytest

from flag_engine.features.constants import STANDARD
from flag_engine.segments.constants import ALL_RULE, EQUAL
from tests.mock_django_classes import (
    DjangoEnvironment,
    DjangoFeature,
    DjangoFeatureSegment,
    DjangoFeatureState,
    DjangoOrganisation,
    DjangoProject,
    DjangoSegment,
    DjangoSegmentCondition,
    DjangoSegmentRule,
)


@pytest.fixture()
def mock_django_project():
    django_organisation = DjangoOrganisation(id=1, name="My org")
    django_project = DjangoProject(
        id=1,
        name="My Project",
        organisation=django_organisation,
    )
    return django_project


@pytest.fixture()
def mock_django_feature(mock_django_project):
    return DjangoFeature(
        id=1, name="my_feature", project=mock_django_project, type=STANDARD
    )


@pytest.fixture()
def mock_nested_environment(mock_django_project, mock_django_feature):
    return DjangoEnvironment(
        id=1,
        project=mock_django_project,
        name="My Environment",
        api_key="api-key",
    )


@pytest.fixture()
def mock_django_segment(
    mocker,
    mock_django_project,
    mock_django_feature,
    random_api_key,
    request,
    mock_nested_environment,
):
    # To avoid circular fixture dependencies we need to use a traditional MagicMock
    # here which just mimics the api_key of the environment. This is such that the
    # python filtering is correct in the `serialize_feature_states` method on the
    # DjangoSegmentSchema.
    mock_environment = mocker.MagicMock(api_key=random_api_key)

    django_segment_condition = DjangoSegmentCondition(
        operator=EQUAL, property="foo", value="bar"
    )
    django_segment_rule = DjangoSegmentRule(
        type=ALL_RULE, conditions=[django_segment_condition]
    )
    django_feature_segment = DjangoFeatureSegment(
        id_=1,
        priority=0,
        environment=mock_environment,
        feature_states=[
            DjangoFeatureState(
                id=2,
                feature=mock_django_feature,
                enabled=True,
                value="overridden for segment",
                environment=mock_nested_environment,
            )
        ],
    )
    django_segment = DjangoSegment(
        id=1,
        name="My Segment",
        rules=[django_segment_rule],
        feature_segments=[django_feature_segment],
    )
    mock_django_project.add_segment(django_segment)

    return django_segment


@pytest.fixture()
def mock_django_environment(
    mock_django_project,
    mock_django_feature,
    mock_django_segment,
    mock_nested_environment,
):
    return DjangoEnvironment(
        id=1,
        project=mock_django_project,
        name="My Environment",
        api_key="api-key",
        feature_states=[
            DjangoFeatureState(
                id=1,
                feature=mock_django_feature,
                enabled=True,
                value="foobar",
                environment=mock_nested_environment,
            )
        ],
    )
