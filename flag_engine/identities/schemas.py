import typing
import uuid

from marshmallow import EXCLUDE, Schema, fields, post_dump

from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.identities.models import IdentityModel
from flag_engine.utils.marshmallow.fields import IdentityFeaturesListField
from flag_engine.utils.marshmallow.schemas import LoadToModelMixin

from .traits.schemas import TraitSchema


class BaseIdentitySchema(Schema):
    identifier = fields.Str()
    created_date = fields.DateTime()
    identity_uuid = fields.UUID(dump_default=uuid.uuid4)
    environment_api_key = fields.Str()

    @post_dump
    def generate_composite_key(self, data: typing.Dict[str, typing.Any], **kwargs):
        data.setdefault(
            "composite_key",
            IdentityModel.generate_composite_key(
                env_key=data["environment_api_key"], identifier=data["identifier"]
            ),
        )
        return data


class IdentitySchema(LoadToModelMixin, BaseIdentitySchema):
    identity_traits = fields.List(fields.Nested(TraitSchema), required=False)
    identity_features = IdentityFeaturesListField(
        fields.Nested(FeatureStateSchema), required=False
    )

    django_id = fields.Int(required=False, allow_none=True)
    composite_key = fields.Str(dump_only=True)

    class Meta:
        unknown = EXCLUDE
        model_class = IdentityModel
