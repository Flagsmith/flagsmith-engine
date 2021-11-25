import typing

from marshmallow import fields, validate

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.utils.marshmallow.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class SegmentConditionSchema(LoadToModelSchema):
    operator = fields.Str(validate=validate.OneOf(constants.CONDITION_OPERATORS))
    property_ = fields.Method(
        serialize="serialize_property",
        deserialize="deserialize_property",
    )
    value = fields.Field()

    class Meta:
        model_class = SegmentConditionModel

    def serialize_property(self, obj: typing.Any) -> str:
        return getattr(obj, "property", None) or getattr(obj, "property_")

    def deserialize_property(self, value: str):
        return value


class SegmentRuleSchema(LoadToModelSchema):
    type = fields.Str(validate=validate.OneOf(constants.RULE_TYPES))
    rules = ListOrDjangoRelatedManagerField(
        fields.Nested("SegmentRuleSchema"), required=False
    )
    conditions = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentConditionSchema), required=False
    )

    class Meta:
        model_class = SegmentRuleModel


class SegmentSchema(LoadToModelSchema):
    id = fields.Int()
    name = fields.Str()
    rules = ListOrDjangoRelatedManagerField(fields.Nested(SegmentRuleSchema))
    feature_states = fields.Method(
        serialize="serialize_feature_states", deserialize="deserialize_feature_states"
    )

    def __init__(self, *args, **kwargs):
        super(SegmentSchema, self).__init__(*args, **kwargs)
        self.feature_state_schema = FeatureStateSchema()

    class Meta:
        model_class = SegmentModel

    def serialize_feature_states(self, instance: typing.Any) -> typing.List[dict]:
        if hasattr(instance, "feature_segments"):
            feature_states = []
            # Django datamodel incorrectly uses a foreign key for the
            # FeatureState -> FeatureSegment relationship so we have to recursively
            # build the list like this
            queryset = instance.feature_segments.order_by("feature", "-priority").all()
            for feature_segment in queryset:
                feature_states.extend(feature_segment.feature_states.all())
            return self.feature_state_schema.dump(feature_states, many=True)
        return getattr(instance, "feature_states", [])

    def deserialize_feature_states(self, value: typing.List[dict]) -> typing.List[dict]:
        return self.feature_state_schema.load(value, many=True)
