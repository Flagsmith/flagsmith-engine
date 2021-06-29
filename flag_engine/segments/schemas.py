from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError,
    post_load,
)

from flag_engine.segments import constants
from flag_engine.segments.models import Segment
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField


class SegmentConditionSchema(Schema):
    operator = fields.Str(validate=validate.OneOf(constants.CONDITION_OPERATORS))
    property_ = fields.Str(data_key="property")
    value = fields.Field()


class SegmentRuleSchema(Schema):
    type = fields.Str(validate=validate.OneOf(constants.RULE_TYPES))
    rules = ListOrDjangoRelatedManagerField(
        fields.Nested("SegmentRuleSchema"), required=False
    )
    conditions = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentConditionSchema), required=False
    )

    @validates_schema()
    def validate_not_rules_and_conditions(self, data, **kwargs):
        if data.get("rules") and data.get("conditions"):
            raise ValidationError(
                "Segment rule must not have both rules and conditions"
            )


class SegmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    rules = ListOrDjangoRelatedManagerField(fields.Nested(SegmentRuleSchema))

    @post_load()
    def make_segment(self, data, **kwargs):
        return Segment(**data)
