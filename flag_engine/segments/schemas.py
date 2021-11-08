import typing

from marshmallow import fields, validate

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
        return getattr(obj, "property", None) or obj["property_"]

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

    class Meta:
        model_class = SegmentModel
