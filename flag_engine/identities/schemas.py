import typing
import uuid

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_dump

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.identities.models import IdentityModel, TraitModel
from flag_engine.utils.marshmallow.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema

from .constants import ACCEPTED_TRAIT_VALUE_TYPES, STRING, TRAIT_STRING_VALUE_MAX_LENGTH


class BaseTraitSchema(Schema):
    trait_key = fields.Str()
    trait_value = fields.Method(
        serialize="serialize_trait_value",
        deserialize="deserialize_trait_value",
        allow_none=True,
    )

    class Meta:
        model_class = TraitModel

    def serialize_trait_value(self, obj: typing.Any) -> int:
        return getattr(obj, "trait_value")

    def deserialize_trait_value(self, trait_value: typing.Any) -> typing.Any:
        data_type = type(trait_value).__name__
        if data_type not in ACCEPTED_TRAIT_VALUE_TYPES:
            trait_value = str(trait_value)
            data_type = STRING
        if data_type == STRING and len(trait_value) > TRAIT_STRING_VALUE_MAX_LENGTH:
            raise ValidationError(
                f"Value string is too long. Must be less than\
                {TRAIT_STRING_VALUE_MAX_LENGTH} character"
            )
        return trait_value


class TraitSchema(LoadToModelSchema, BaseTraitSchema):
    class Meta:
        model_class = TraitModel


class IdentitySchemaLoad(LoadToModelSchema):
    identifier = fields.Str()
    created_date = fields.DateTime()
    identity_uuid = fields.UUID(default=uuid.uuid4)
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
