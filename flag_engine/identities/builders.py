from typing import Any, Dict

from flag_engine.identities.models import IdentityModel


def build_identity_dict(identity_model: IdentityModel) -> Dict[str, Any]:
    return identity_model.dict()


def build_identity_model(identity_dict: Dict[str, Any]) -> IdentityModel:
    return IdentityModel.parse_obj(identity_dict)
