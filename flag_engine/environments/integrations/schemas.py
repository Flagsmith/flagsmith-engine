from marshmallow import fields

from flag_engine.environments.integrations.models import IntegrationModel
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class IntegrationSchema(LoadToModelSchema):
    api_key = fields.Str(required=False, allow_none=True)
    base_url = fields.Str(required=False, allow_none=True)
    entity_selector = fields.Str(required=False, allow_none=True)

    class Meta:
        model_class = IntegrationModel
