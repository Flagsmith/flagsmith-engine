from marshmallow import Schema, fields, post_load

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.identities.models import Trait, Identity


class TraitSchema(Schema):
    key = fields.Str()
    value = fields.Str()

    @post_load
    def make_trait(self, data, **kwargs):
        return Trait(**data)


class IdentitySchema(Schema):
    identifier = fields.Str()
    created_date = fields.Date()
    environment_id = fields.Integer()
    environment_api_key = fields.Str()
    traits = fields.List(fields.Nested(TraitSchema))
    identity_flags = fields.List(fields.Nested(FeatureStateSchema))

    @post_load
    def make_identity(self, data, **kwargs):
        return Identity(**data)
