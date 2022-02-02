from flag_engine.django_transform.schemas import (
    DjangoEnvironmentSchema,
    DjangoSegmentConditionSchema,
    DjangoSegmentSchema,
)
from flag_engine.segments.constants import PERCENTAGE_SPLIT
from tests.mock_django_classes import DjangoSegmentCondition


def test_environment_schema_dump_sets_api_key_in_context(django_environment):
    # Given
    schema = DjangoEnvironmentSchema()

    # When
    environment_data = schema.dump(django_environment)

    # Then
    assert environment_data
    assert schema.context.get("environment_api_key") == django_environment.api_key


def test_segment_condition_schema_dump_when_property_is_none():
    # Given
    schema = DjangoSegmentConditionSchema()
    mock_django_segment_condition = DjangoSegmentCondition(
        operator=PERCENTAGE_SPLIT, value=10
    )

    # When
    data = schema.dump(mock_django_segment_condition)

    # Then
    assert data["value"] == mock_django_segment_condition.value
    assert data["operator"] == mock_django_segment_condition.operator
    assert data["property_"] is None


def test_segment_schema_serialize_feature_states(mocker):
    # Given
    # a mock feature state schema object so we can confirm that dump is
    # called correctly later on
    mock_feature_state_schema_class = mocker.patch(
        "flag_engine.django_transform.schemas.DjangoFeatureStateSchema"
    )
    mock_feature_state_schema = mock_feature_state_schema_class.return_value

    # and we instantiate the segment schema with the environment_api_key in the context
    environment_api_key = "api-key"
    schema = DjangoSegmentSchema(context={"environment_api_key": environment_api_key})

    # and we create some mock objects
    mock_environment = mocker.MagicMock(api_key=environment_api_key)
    mock_segment = mocker.MagicMock()
    mock_feature_state = mocker.MagicMock()
    mock_feature_segment = mocker.MagicMock(environment=mock_environment)
    mock_feature_segments = [mock_feature_segment]

    # and set up the return values as per django queryset logic
    mock_segment.feature_segments.all.return_value = mock_feature_segments
    mock_feature_segment.feature_states.all.return_value = [mock_feature_state]

    # and we mock the sort_and_filter function to return the same set of feature
    # segments
    mock_sort_and_filter_feature_segments = mocker.patch(
        "flag_engine.django_transform.schemas.sort_and_filter_feature_segments",
        return_value=mock_feature_segments,
    )

    # When
    serialized_instance = schema.serialize_feature_states(mock_segment)

    # Then
    # The feature segments are filtered correctly by the environment
    mock_segment.feature_segments.all.assert_called_once_with()

    # and the feature states are dumped and returned correctly
    mock_feature_state_schema.dump.assert_called_once()
    mock_feature_state_schema.dump.assert_called_with([mock_feature_state], many=True)
    assert serialized_instance == mock_feature_state_schema.dump.return_value

    # and the sort and filter function is called with the correct inputs
    mock_sort_and_filter_feature_segments.assert_called_once_with(
        mock_feature_segments, environment_api_key
    )
