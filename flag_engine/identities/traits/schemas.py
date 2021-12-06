from marshmallow import fields

from flag_engine.identities.traits.models import TraitModel
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class TraitSchema(LoadToModelSchema):
    trait_key = fields.Str()
    trait_value = fields.Field(allow_none=True)

    class Meta:
        model_class = TraitModel
