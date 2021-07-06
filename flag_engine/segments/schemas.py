from marshmallow import Schema, fields, post_load, validate

from flag_engine.segments import constants
from flag_engine.segments.models import SegmentModel
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField


class SegmentConditionSchema(Schema):
    operator = fields.Str(validate=validate.OneOf(constants.CONDITION_OPERATORS))
    property_ = fields.Str(attribute="property")
    value = fields.Field()


class SegmentRuleSchema(Schema):
    type = fields.Str(validate=validate.OneOf(constants.RULE_TYPES))
    rules = ListOrDjangoRelatedManagerField(
        fields.Nested("SegmentRuleSchema"), required=False
    )
    conditions = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentConditionSchema), required=False
    )


class SegmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    rules = ListOrDjangoRelatedManagerField(fields.Nested(SegmentRuleSchema))

    @post_load()
    def make_segment(self, data, **kwargs):
        return SegmentModel(**data)
