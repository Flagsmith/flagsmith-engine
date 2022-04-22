import decimal

from marshmallow import fields

from flag_engine.identities.traits.models import TraitModel
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class TraitValueField(fields.Field):
    """Field that serializes float(and only float) to Decimal(because dynamodb can't understand float)
    and deserializes Decimal(and only decimal) to float
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if type(value) is float:
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
