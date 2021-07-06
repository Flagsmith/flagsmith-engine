from marshmallow import Schema, fields, post_load

from flag_engine.environments.integrations.models import IntegrationModel


class IntegrationSchema(Schema):
    api_key = fields.Str(required=False, allow_none=True)
    base_url = fields.Str(required=False, allow_none=True)

    @post_load()
    def make_integration_model(self, data, **kwargs):
        return IntegrationModel(**data)
