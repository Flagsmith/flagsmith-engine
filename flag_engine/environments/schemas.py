from marshmallow import EXCLUDE, Schema, fields

from flag_engine.environments.integrations.schemas import IntegrationSchema
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.projects.schemas import ProjectSchema
from flag_engine.utils.marshmallow.schemas import LoadToModelMixin


class BaseEnvironmentSchema(Schema):
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
