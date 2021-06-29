from marshmallow import Schema, fields, post_load

from flag_engine.projects.models import Project
from flag_engine.segments.schemas import SegmentSchema
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField


class ProjectSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    segments = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentSchema), required=False
    )

    @post_load()
    def make_project(self, data, **kwargs) -> Project:
        return Project(**data)
