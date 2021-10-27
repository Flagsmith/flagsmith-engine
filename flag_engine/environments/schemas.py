from marshmallow import fields

from flag_engine.environments.integrations.schemas import IntegrationSchema
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.projects.schemas import ProjectSchema
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schema import LoadToModelSchema


class EnvironmentSchema(LoadToModelSchema):
    model_class = EnvironmentModel
    id = fields.Int()
    api_key = fields.Str()
    feature_states = ListOrDjangoRelatedManagerField(
        fields.Nested(FeatureStateSchema),
        metadata={"filter_kwargs": {"feature_segment_id": None, "identity_id": None}},
    )
    project = fields.Nested(ProjectSchema)

    segment_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    heap_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    mixpanel_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    amplitude_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
