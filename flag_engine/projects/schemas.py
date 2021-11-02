from marshmallow import fields

from flag_engine.organisations.schemas import OrganisationSchema
from flag_engine.projects.models import ProjectModel
from flag_engine.segments.schemas import SegmentSchema
from flag_engine.utils.marshmallow.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class ProjectSchema(LoadToModelSchema):
    id = fields.Int()
    name = fields.Str()
    segments = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentSchema), required=False
    )
    organisation = fields.Nested(OrganisationSchema)
    hide_disabled_flags = fields.Bool()

    class Meta:
        model_class = ProjectModel
