from marshmallow import Schema, fields, post_load

from flag_engine.environments.models import Environment
from flag_engine.features.schemas import FeatureStateSchema
from flag_engine.projects.schemas import ProjectSchema
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField


class EnvironmentSchema(Schema):
    id = fields.Int()
    api_key = fields.Str()
    feature_states = ListOrDjangoRelatedManagerField(fields.Nested(FeatureStateSchema))
    project = fields.Nested(ProjectSchema)

    @post_load()
    def make_environment(self, data: dict, **kwargs) -> Environment:
        return Environment(**data)
