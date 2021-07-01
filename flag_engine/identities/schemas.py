from marshmallow import Schema, fields, post_load

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.identities.models import Identity, Trait


class TraitSchema(Schema):
    key = fields.Str()
    value = fields.Str()

    @post_load
    def make_trait(self, data, **kwargs):
        return Trait(**data)


class IdentitySchema(Schema):
    id = fields.Int()
    identifier = fields.Str()
    created_date = fields.Date()
    environment_id = fields.Method(
        serialize="serialize_environment_id", deserialize="deserialize_environment_id"
    )
    environment_api_key = fields.Str()
    traits = fields.List(fields.Nested(TraitSchema))
    identity_flags = fields.List(fields.Nested(FeatureStateSchema))

    @post_load
    def make_identity(self, data, **kwargs):
        return Identity(**data)

    def serialize_environment_id(self, obj: object) -> int:
        if isinstance(obj, dict):
            return obj["environment_id"]

        return obj.environment.id

    def deserialize_environment_id(self, environment_id: int) -> int:
        return environment_id
