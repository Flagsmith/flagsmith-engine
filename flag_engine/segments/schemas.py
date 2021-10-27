from marshmallow import fields, validate

from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.utils.marshmallow.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schema import LoadToModelSchema


class SegmentConditionSchema(LoadToModelSchema):
    model_class = SegmentConditionModel
    operator = fields.Str(validate=validate.OneOf(constants.CONDITION_OPERATORS))
    property_ = fields.Str(attribute="property")
    value = fields.Field()


class SegmentRuleSchema(LoadToModelSchema):
    model_class = SegmentRuleModel
    type = fields.Str(validate=validate.OneOf(constants.RULE_TYPES))
    rules = ListOrDjangoRelatedManagerField(
        fields.Nested("SegmentRuleSchema"), required=False
    )
    conditions = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentConditionSchema), required=False
    )


class SegmentSchema(LoadToModelSchema):
    model_class = SegmentModel
    id = fields.Int()
    name = fields.Str()
    rules = ListOrDjangoRelatedManagerField(fields.Nested(SegmentRuleSchema))
