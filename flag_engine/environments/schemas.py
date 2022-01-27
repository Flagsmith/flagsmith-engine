from marshmallow import EXCLUDE, Schema, fields

from flag_engine.environments.integrations.schemas import IntegrationSchema
from flag_engine.environments.models import EnvironmentAPIKeyModel, EnvironmentModel
from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.projects.schemas import ProjectSchema
from flag_engine.utils.marshmallow.schemas import LoadToModelMixin


class BaseEnvironmentAPIKeySchema(Schema):
    id = fields.Int()
    key = fields.Str()
    created_at = fields.DateTime()
    name = fields.Str()
    expires_at = fields.DateTime()
    active = fields.Bool()


class EnvironmentAPIKeySchema(LoadToModelMixin, Schema):
    client_api_key = fields.Str()

    class Meta:
        model_class = EnvironmentAPIKeyModel


class BaseEnvironmentSchema(Schema):
    id = fields.Int()
    api_key = fields.Str()
    segment_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    heap_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    mixpanel_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    amplitude_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)


class EnvironmentSchema(LoadToModelMixin, BaseEnvironmentSchema):
    feature_states = fields.List(fields.Nested(FeatureStateSchema))
    project = fields.Nested(ProjectSchema)

    class Meta:
        model_class = EnvironmentModel
        unknown = EXCLUDE
