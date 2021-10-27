import typing
from datetime import datetime

from marshmallow import EXCLUDE, fields, post_dump, utils

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.identities.models import IdentityModel, TraitModel
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schema import LoadToModelSchema


class TraitSchema(LoadToModelSchema):
    model_class = TraitModel
    trait_key = fields.Str()
    trait_value = fields.Str()


class IdentitySchema(LoadToModelSchema):
    model_class = IdentityModel
    id = fields.Int()
    identifier = fields.Str()
    composite_key = fields.Str(dump_only=True)
    created_date = fields.Method(
        serialize="serialize_created_date",
        deserialize="deserialize_created_date",
    )
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
        # to exclude dump only fields, e.g: composite_key
        unknown = EXCLUDE

    @post_dump
    def generate_composite_key(self, data, **kwargs):
        data["composite_key"] = f"{data['environment_api_key']}_{data['identifier']}"
        return data

    def serialize_environment_api_key(self, obj: typing.Any) -> int:
        if hasattr(obj, "environment"):
            return obj.environment.api_key

        return getattr(obj, "environment_api_key", None) or obj["environment_api_key"]

    def deserialize_environment_api_key(self, environment_api_key: int) -> int:
        return environment_api_key

    def serialize_created_date(self, obj: typing.Any) -> str:
        created_date = getattr(obj, "created_date", None) or obj["created_date"]
        if isinstance(created_date, str):
            return created_date
        return created_date.isoformat()

    def deserialize_created_date(self, created_date: str) -> datetime:
        return utils.from_iso_datetime(created_date)
