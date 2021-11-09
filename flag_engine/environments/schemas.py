from marshmallow import fields, pre_dump

from flag_engine.environments.integrations.schemas import IntegrationSchema
from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.projects.schemas import ProjectSchema
from flag_engine.utils.marshmallow.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class EnvironmentSchema(LoadToModelSchema):
    id = fields.Int()
    api_key = fields.Str()
    _all_feature_states = ListOrDjangoRelatedManagerField(
        fields.Nested(FeatureStateSchema)
    )
    project = fields.Nested(ProjectSchema)
    segment_overrides = ListOrDjangoRelatedManagerField(
        fields.Nested(FeatureStateSchema),
        metadata={
            "filter_kwargs": {"feature_segment_id__isnull": False, "identity_id": None}
        },
    )
    segment_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    heap_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    mixpanel_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)
    amplitude_config = fields.Nested(IntegrationSchema, required=False, allow_none=True)

    class Meta:
        model_class = EnvironmentModel

    @pre_dump()
    def add_segment_overrides(self, obj, *args, **kwargs):
        if hasattr(obj, "feature_states"):
            obj.segment_overrides = obj.feature_states
        return obj
