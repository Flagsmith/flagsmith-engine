from marshmallow import Schema

from flag_engine.identities.models import IdentityModel
from flag_engine.identities.schemas import IdentitySchema

identity_schema = IdentitySchema()


def build_identity_dict(
    identity_model: IdentityModel, schema: Schema = identity_schema
) -> dict:
    return schema.dump(identity_model)


def build_identity_model(identity_dict: dict) -> IdentityModel:
    return identity_schema.load(identity_dict)
