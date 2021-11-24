import typing

from marshmallow import EXCLUDE, fields, post_dump

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.identities.models import IdentityModel, TraitModel
from flag_engine.utils.marshmallow.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class TraitSchema(LoadToModelSchema):
    trait_key = fields.Str()
    trait_value = fields.Str()

    class Meta:
        model_class = TraitModel


class IdentitySchemaLoad(LoadToModelSchema):
    identifier = fields.Str()
    created_date = fields.DateTime()
    environment_api_key = fields.Method(
        serialize="serialize_environment_api_key",
        deserialize="deserialize_environment_api_key",
    )
    identity_traits = ListOrDjangoRelatedManagerField(
        fields.Nested(TraitSchema), required=False
    )
    identity_features = ListOrDjangoRelatedManagerField(
        fields.Nested(FeatureStateSchema), required=False
    )

    class Meta:
        unknown = EXCLUDE
        model_class = IdentityModel

    @post_dump
    def generate_composite_key(self, data: typing.Dict[str, typing.Any], **kwargs):
        data.setdefault(
            "composite_key",
            IdentityModel.generate_composite_key(
                env_key=data["environment_api_key"], identifier=data["identifier"]
            ),
        )
        return data

    def serialize_environment_api_key(self, obj: typing.Any) -> int:
        if hasattr(obj, "environment"):
            return obj.environment.api_key

        return getattr(obj, "environment_api_key", None)

    def deserialize_environment_api_key(self, environment_api_key: str) -> str:
        return environment_api_key


class IdentitySchemaDump(IdentitySchemaLoad):
    class Meta:
        unknown = EXCLUDE
        model_class = IdentityModel

    composite_key = fields.Str(dump_only=True)
    django_id = fields.Int(required=False, attribute="id", dump_only=True)
