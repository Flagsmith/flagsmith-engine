from marshmallow import Schema, fields, post_load

from flag_engine.organisations.schemas import OrganisationSchema
from flag_engine.projects.models import ProjectModel
from flag_engine.segments.schemas import SegmentSchema
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField


class ProjectSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    segments = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentSchema), required=False
    )
    organisation = fields.Nested(OrganisationSchema)
    hide_disabled_flags = fields.Bool()

    @post_load()
    def make_project(self, data, **kwargs) -> ProjectModel:
        return ProjectModel(**data)
