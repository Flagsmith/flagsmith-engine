from marshmallow import fields

from flag_engine.organisations.models import OrganisationModel
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class OrganisationSchema(LoadToModelSchema):
    id = fields.Int()
    name = fields.Str()
    stop_serving_flags = fields.Boolean()
    persist_trait_data = fields.Boolean()
    feature_analytics = fields.Boolean()

    class Meta:
        model_class = OrganisationModel
