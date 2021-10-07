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
    environment_api_key = fields.Method(
        serialize="serialize_environment_api_key",
        deserialize="deserialize_environment_api_key",
    )
    identity_traits = ListOrDjangoRelatedManagerField(
        fields.Nested(TraitSchema), required=False
    )
    identity_features = ListOrDjangoRelatedManagerField(
        fields.Nested(FeatureStateSchema),
        required=False,
        metadata={
            "filter_kwargs": {"feature_segment_id": None, "identity_id__isnull": None}
        },
    )

    @post_load
    def make_identity(self, data, **kwargs):
        return IdentityModel(**data)

    def serialize_environment_api_key(self, obj: typing.Any) -> int:
        if hasattr(obj, "environment"):
            return obj.environment.api_key

        return getattr(obj, "environment_api_key", None) or obj["environment_api_key"]

    def deserialize_environment_api_key(self, environment_api_key: int) -> int:
        return environment_api_key
