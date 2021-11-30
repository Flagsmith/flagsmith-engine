from flag_engine.features.constants import STANDARD
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.segments.constants import ALL_RULE, EQUAL, PERCENTAGE_SPLIT
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.segments.schemas import SegmentConditionSchema, SegmentSchema
from tests.mock_django_classes import (
    DjangoFeature,
    DjangoFeatureSegment,
    DjangoFeatureState,
    DjangoSegment,
    DjangoSegmentCondition,
    DjangoSegmentRule,
)

segment_schema = SegmentSchema()


def test_segment_schema_django_object_to_dict(django_project):
    # Given
    segment = DjangoSegment(
        id=1,
        name="Segment",
        rules=[
            DjangoSegmentRule(
                type=ALL_RULE,
                conditions=[
                    DjangoSegmentCondition(operator=EQUAL, property="foo", value="bar")
                ],
            )
        ],
        feature_segments=[
            DjangoFeatureSegment(
                feature_states=[
                    DjangoFeatureState(
                        id=1,
                        feature=DjangoFeature(
                            id=1,
                            name="my_feature",
                            project=django_project,
                            type=STANDARD,
                        ),
                        enabled=True,
                    )
                ]
            )
        ],
    )

    schema = SegmentSchema(context={"environment_api_key": "api-key"})

    # When
    data = schema.dump(segment)

    # Then
    assert data["id"] == segment.id
    assert len(data["feature_states"]) == 1
    assert len(data["rules"]) == 1


def test_segment_schema_engine_model_object_to_dict(project):
    # Given
    segment = SegmentModel(
        id=1,
        name="Segment",
        rules=[
            SegmentRuleModel(
                type=ALL_RULE,
                conditions=[
                    SegmentConditionModel(operator=EQUAL, property_="foo", value="bar")
                ],
            )
        ],
        feature_states=[
            FeatureStateModel(
                id=1,
                feature=FeatureModel(
                    id=1,
                    name="my_feature",
                    type=STANDARD,
                ),
                enabled=True,
            )
        ],
    )

    # When
    data = segment_schema.dump(segment)

    # Then
    assert data["id"] == segment.id
    assert len(data["feature_states"]) == 1
    assert len(data["rules"]) == 1


def test_dict_to_segment_model():
    # Given
    segment_dict = {
        "id": 1,
        "name": "Segment",
        "rules": [
            {
                "rules": [],
                "conditions": [
                    {"operator": "EQUAL", "property_": "foo", "value": "bar"}
                ],
                "type": "ALL",
            }
        ],
        "feature_states": [
            {
                "multivariate_feature_state_values": [],
                "id": 1,
                "segment_id": None,
                "enabled": True,
                "feature_state_value": None,
                "feature": {"id": 1, "name": "my_feature", "type": "STANDARD"},
            }
        ],
    }

    # When
    segment_model = segment_schema.load(segment_dict)

    # Then
    assert isinstance(segment_model, SegmentModel)
    assert segment_model.id == segment_dict["id"]
    assert len(segment_model.rules) == 1
    assert len(segment_model.feature_states) == 1


def test_segment_condition_schema_dump_when_property_is_none():
    # Given
    schema = SegmentConditionSchema()
    mock_django_segment_condition = DjangoSegmentCondition(
        operator=PERCENTAGE_SPLIT, value=10
    )

    # When
    data = schema.dump(mock_django_segment_condition)

    # Then
    assert data["value"] == mock_django_segment_condition.value
    assert data["operator"] == mock_django_segment_condition.operator
    assert data["property_"] is None


def test_segment_condition_schema_load_when_property_is_none():
    # Given
    schema = SegmentConditionSchema()
    data = {"operator": PERCENTAGE_SPLIT, "value": 10, "property_": None}

    # When
    segment_condition_model = schema.load(data)

    # Then
    assert segment_condition_model.value == data["value"]
    assert segment_condition_model.operator == data["operator"]
    assert segment_condition_model.property_ is None


def test_segment_schema_serialize_feature_states(mocker):
    # Given
    # a mock feature state schema object so we can confirm that dump is
    # called correctly later on
    mock_feature_state_schema_class = mocker.patch(
        "flag_engine.segments.schemas.FeatureStateSchema"
    )
    mock_feature_state_schema = mock_feature_state_schema_class.return_value

    # and we instantiate the segment schema with the environment_api_key in the context
    environment_api_key = "api-key"
    schema = SegmentSchema(context={"environment_api_key": environment_api_key})

    # and we create some mock objects
    mock_segment = mocker.MagicMock()
    mock_feature_state = mocker.MagicMock()
    mock_feature_segment = mocker.MagicMock()

    # and set up the return values as per django queryset logic
    order_by_response = mock_segment.feature_segments.order_by.return_value
    mock_feature_segment.feature_states.all.return_value = [mock_feature_state]
    order_by_response.filter.return_value = [mock_feature_segment]

    # When
    serialized_instance = schema.serialize_feature_states(mock_segment)

    # Then
    # The feature segments are filtered correctly by the environment
    mock_segment.feature_segments.order_by.assert_called_once_with(
        "feature", "-priority"
    )
    order_by_response.filter.assert_called_once_with(
        environment__api_key=environment_api_key
    )

    # and the feature states are dumped and returned correctly
    mock_feature_state_schema.dump.assert_called_once()
    mock_feature_state_schema.dump.assert_called_with([mock_feature_state], many=True)
    assert serialized_instance == mock_feature_state_schema.dump.return_value
