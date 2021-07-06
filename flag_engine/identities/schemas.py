import typing

from marshmallow import Schema, fields, post_load

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.identities.models import IdentityModel, TraitModel
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField


class TraitSchema(Schema):
    trait_key = fields.Str()
    trait_value = fields.Str()

    @post_load
    def make_trait(self, data, **kwargs):
        return TraitModel(**data)


class IdentitySchema(Schema):
    id = fields.Int()
    identifier = fields.Str()
    created_date = fields.AwareDateTime()
    environment_id = fields.Method(
        serialize="serialize_environment_id", deserialize="deserialize_environment_id"
    )
    identity_traits = ListOrDjangoRelatedManagerField(
        fields.Nested(TraitSchema), required=False
    )
    identity_features = ListOrDjangoRelatedManagerField(
        fields.Nested(FeatureStateSchema), required=False
    )

    @post_load
    def make_identity(self, data, **kwargs):
        return IdentityModel(**data)

    def serialize_environment_id(self, obj: typing.Any) -> int:
        if hasattr(obj, "environment"):
            return obj.environment.id

        return getattr(obj, "environment_id", None) or obj["environment_id"]

    def deserialize_environment_id(self, environment_id: int) -> int:
        return environment_id
