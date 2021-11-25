from flag_engine.features.constants import STANDARD
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.segments.constants import ALL_RULE, EQUAL
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.segments.schemas import SegmentSchema
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

    # When
    data = segment_schema.dump(segment)

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
