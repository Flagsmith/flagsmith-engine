import typing

from flag_engine.identities.models import IdentityModel
from flag_engine.identities.schemas import IdentitySchema

identity_schema = IdentitySchema()


def build_identity_dict(identity_obj: typing.Any) -> dict:
    return identity_schema.dump(identity_obj)


def build_identity_model(identity_obj: typing.Any) -> IdentityModel:
    return identity_schema.load(build_identity_dict(identity_obj))
