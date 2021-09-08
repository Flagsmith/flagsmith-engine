from marshmallow import Schema, fields, post_load

from flag_engine.organisations.models import OrganisationModel


class OrganisationSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    stop_serving_flags = fields.Boolean()
    persist_trait_data = fields.Boolean()
    feature_analytics = fields.Boolean()

    @post_load()
    def make_organisation(self, data, **kwargs) -> OrganisationModel:
        return OrganisationModel(**data)
