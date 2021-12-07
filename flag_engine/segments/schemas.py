from marshmallow import Schema, fields, validate

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.utils.marshmallow.schemas import LoadToModelMixin


class BaseSegmentConditionSchema(Schema):
    operator = fields.Str(validate=validate.OneOf(constants.CONDITION_OPERATORS))
    value = fields.Field()


class SegmentConditionSchema(LoadToModelMixin, BaseSegmentConditionSchema):
    property_ = fields.Str(allow_none=True)

    class Meta:
        model_class = SegmentConditionModel


class BaseSegmentRuleSchema(Schema):
    type = fields.Str(validate=validate.OneOf(constants.RULE_TYPES))


class SegmentRuleSchema(LoadToModelMixin, BaseSegmentRuleSchema):
    rules = fields.List(fields.Nested("SegmentRuleSchema"), required=False)
    conditions = fields.List(fields.Nested(SegmentConditionSchema), required=False)

    class Meta:
        model_class = SegmentRuleModel


class BaseSegmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    django_id = fields.Int(required=False, allow_none=True)


class SegmentSchema(LoadToModelMixin, BaseSegmentSchema):
    rules = fields.List(fields.Nested(SegmentRuleSchema))
    feature_states = fields.List(fields.Nested(FeatureStateSchema))

    class Meta:
        model_class = SegmentModel
