from marshmallow import EXCLUDE, Schema, fields

from flag_engine.environments.integrations.schemas import IntegrationSchema
from flag_engine.environments.models import (
    EnvironmentAPIKeyModel,
    EnvironmentModel,
    WebhookModel,
)
from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.projects.schemas import ProjectSchema
from flag_engine.utils.marshmallow.schemas import LoadToModelMixin, LoadToModelSchema


class BaseEnvironmentAPIKeySchema(Schema):
    id = fields.Int()
    key = fields.Str()
    created_at = fields.DateTime()
    name = fields.Str()
    active = fields.Bool()
    expires_at = fields.DateTime(allow_none=True)


class EnvironmentAPIKeySchema(LoadToModelMixin, BaseEnvironmentAPIKeySchema):
    client_api_key = fields.Str()

    class Meta:
        model_class = EnvironmentAPIKeyModel


class WebhookSchema(LoadToModelSchema):
    enabled = fields.Bool()
    url = fields.URL()
    secret = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        model_class = WebhookModel


class BaseEnvironmentSchema(Schema):
    id = fields.Int()
    api_key = fields.Str()
    segment_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    heap_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    mixpanel_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    amplitude_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    dynatrace_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)


class EnvironmentSchema(LoadToModelMixin, BaseEnvironmentSchema):
    feature_states = fields.List(fields.Nested(FeatureStateSchema))
    project = fields.Nested(ProjectSchema)
    webhooks = fields.List(
        fields.Nested(WebhookSchema), required=False, allow_none=True
    )

    class Meta:
        model_class = EnvironmentModel
        unknown = EXCLUDE
