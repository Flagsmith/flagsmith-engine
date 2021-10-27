from marshmallow import fields

from flag_engine.organisations.schemas import OrganisationSchema
from flag_engine.projects.models import ProjectModel
from flag_engine.segments.schemas import SegmentSchema
from flag_engine.utils.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schema import LoadToModelSchema


class ProjectSchema(LoadToModelSchema):
    model_class = ProjectModel
    id = fields.Int()
    name = fields.Str()
    segments = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentSchema), required=False
    )
    organisation = fields.Nested(OrganisationSchema)
    hide_disabled_flags = fields.Bool()
