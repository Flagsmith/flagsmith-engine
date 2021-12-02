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
def mock_django_segment(mock_django_project, mock_django_feature):
    django_segment_condition = DjangoSegmentCondition(
        operator=EQUAL, property="foo", value="bar"
    )
    django_segment_rule = DjangoSegmentRule(
        type=ALL_RULE, conditions=[django_segment_condition]
    )
    django_feature_segment = DjangoFeatureSegment(
        feature_states=[
            DjangoFeatureState(
                id=2,
                feature=mock_django_feature,
                enabled=True,
                value="overridden for segment",
            )
        ]
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
    mock_django_project, mock_django_feature, mock_django_segment
):
    return DjangoEnvironment(
        id=1,
        project=mock_django_project,
        name="My Environment",
        api_key="api-key",
        feature_states=[
            DjangoFeatureState(
                id=1, feature=mock_django_feature, enabled=True, value="foobar"
            )
        ],
    )
