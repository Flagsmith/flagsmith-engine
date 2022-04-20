import pytest
from marshmallow import ValidationError

from flag_engine.api.constants import TRAIT_STRING_VALUE_MAX_LENGTH
from flag_engine.api.schemas import APITraitSchema


def test_loading_trait_value_longer_than_trait_string_value_max_length_raises_validation_error():
    # Given
    schema = APITraitSchema()
    data = {
        "trait_key": "trait_key",
        "trait_value": "i" * (TRAIT_STRING_VALUE_MAX_LENGTH + 1),
    }
    # Then
    with pytest.raises(ValidationError):
        schema.load(data)


@pytest.mark.parametrize(
    "value, deserialized_value",
    (
        ("1", "1"),
        (1.1, 1.1),
        (True, True),
        (-1, -1),
        ({"key": "value"}, str({"key": "value"})),
    ),
)
def test_loading_valid_trait_value_works(value, deserialized_value):
    # Given
    schema = APITraitSchema()
    data = {
        "trait_key": "trait_key",
        "trait_value": value,
    }
    # When
    trait = schema.load(data)
    # Then
    assert trait.trait_value == deserialized_value
