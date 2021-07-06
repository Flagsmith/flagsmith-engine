from flag_engine.identities.models import IdentityModel
from flag_engine.identities.schemas import IdentitySchema

identity_schema = IdentitySchema()


def build_identity_model(identity_obj: object) -> IdentityModel:
    identity_data = identity_schema.dump(identity_obj)
    return identity_schema.load(identity_data)
