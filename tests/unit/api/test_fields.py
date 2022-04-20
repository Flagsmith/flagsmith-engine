import pytest

from flag_engine.api.fields import APITraitValueField


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
def test_api_trait_value_field_deserialize(value, deserialized_value):
    field = APITraitValueField()
    assert field.deserialize(value) == deserialized_value
