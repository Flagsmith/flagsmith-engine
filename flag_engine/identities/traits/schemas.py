import decimal

from marshmallow import fields, post_load

from flag_engine.identities.traits.models import TraitModel
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema
from flag_engine.utils.models import FlagsmithValue, FlagsmithValueType


class TraitValueField(fields.Field):
    """Field that serializes float(and only float) to Decimal(because dynamodb can't understand float)
    and deserializes Decimal(and only decimal) to float
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, FlagsmithValue):
            if value.value_type == FlagsmithValueType.FLOAT:
                return decimal.Decimal(str(value.value))
            elif value.value_type == FlagsmithValueType.BOOLEAN:
                return value.value == "True"
            elif value.value_type == FlagsmithValueType.INTEGER:
                return int(value.value)
            return value.value
        elif isinstance(value, float):
            value = decimal.Decimal(str(value))
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, decimal.Decimal):
            value = float(value)
        return value


class TraitSchema(LoadToModelSchema):
    trait_key = fields.Str()
    trait_value = TraitValueField(allow_none=True)

    class Meta:
        model_class = TraitModel

    @post_load()
    def make_instance(self, data, **kwargs) -> object:
        flagsmith_value = FlagsmithValue.from_untyped_value(
            data.pop("trait_value", None)
        )
        data["trait_value"] = flagsmith_value
        return super(TraitSchema, self).make_instance(data, **kwargs)
