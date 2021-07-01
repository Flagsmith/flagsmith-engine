from marshmallow import Schema, fields, post_load

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.identities.models import Identity, Trait
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField


class TraitSchema(Schema):
    trait_key = fields.Str()
    trait_value = fields.Str()

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
    traits = ListOrDjangoRelatedManagerField(fields.Nested(TraitSchema), required=False)
    identity_features = ListOrDjangoRelatedManagerField(
        fields.Nested(FeatureStateSchema), required=False
    )

    @post_load
    def make_identity(self, data, **kwargs):
        return Identity(**data)

    def serialize_environment_id(self, obj: object) -> int:
        if isinstance(obj, dict):
            return obj["environment_id"]

        return obj.environment.id

    def deserialize_environment_id(self, environment_id: int) -> int:
        return environment_id
