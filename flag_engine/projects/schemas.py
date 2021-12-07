from marshmallow import EXCLUDE, Schema, fields

from flag_engine.organisations.schemas import OrganisationSchema
from flag_engine.projects.models import ProjectModel
from flag_engine.segments.schemas import SegmentSchema
from flag_engine.utils.marshmallow.schemas import LoadToModelMixin


class BaseProjectSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    organisation = fields.Nested(OrganisationSchema)
    hide_disabled_flags = fields.Bool()


class ProjectSchema(LoadToModelMixin, BaseProjectSchema):
    segments = fields.List(fields.Nested(SegmentSchema), required=False)

    class Meta:
        unknown = EXCLUDE
        model_class = ProjectModel
