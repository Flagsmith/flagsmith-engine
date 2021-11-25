import typing

from flag_engine.identities.models import IdentityModel
from flag_engine.identities.schemas import IdentitySchemaDump, IdentitySchemaLoad

identity_schema_load = IdentitySchemaLoad()
identity_schema_dump = IdentitySchemaDump()


def build_identity_dict(identity_obj: typing.Any) -> dict:
    return identity_schema_dump.dump(identity_obj)


def build_identity_model(identity_dict: dict) -> IdentityModel:
    return identity_schema_load.load(identity_dict)
