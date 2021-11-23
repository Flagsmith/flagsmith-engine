from marshmallow import Schema, fields

from flag_engine.environments.integrations.schemas import IntegrationSchema
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.projects.schemas import ProjectSchema
from flag_engine.utils.marshmallow.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class EnvironmentSchemaDump(Schema):
    id = fields.Int()
    api_key = fields.Str()
    _all_feature_states = ListOrDjangoRelatedManagerField(
        fields.Nested(FeatureStateSchema),
        attribute="feature_states",
    )
    project = fields.Nested(ProjectSchema)
    segment_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    heap_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    mixpanel_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    amplitude_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)

    class Meta:
        model_class = EnvironmentModel


class EnvironmentSchemaLoad(EnvironmentSchemaDump, LoadToModelSchema):
    _all_feature_states = ListOrDjangoRelatedManagerField(
        fields.Nested(FeatureStateSchema),
    )

    class Meta:
        model_class = EnvironmentModel
