import json

from flag_engine.django_transform.document_builders import build_identity_document
from flag_engine.utils.json.encoders import DecimalEncoder


def test_build_identity_document(django_identity):
    # When
    identity_dict = build_identity_document(django_identity)

    # Then
    assert (
        identity_dict["composite_key"]
        == f"{django_identity.environment.api_key}_{django_identity.identifier}"
    )
    assert isinstance(identity_dict, dict)
    assert json.dumps(identity_dict, cls=DecimalEncoder)
    assert identity_dict["django_id"] == django_identity.id
    assert identity_dict["identity_uuid"] is not None
