from marshmallow import fields

from flag_engine.utils.collections import IdentityFeaturesList
from flag_engine.utils.marshmallow.fields import IdentityFeaturesListField


def test_identity_features_list_field_serialize():
    # Given
    field = IdentityFeaturesListField(fields.Int())
    # When
    value = field.deserialize([1, 2, 3])
    # Then
    assert isinstance(value, IdentityFeaturesList)
