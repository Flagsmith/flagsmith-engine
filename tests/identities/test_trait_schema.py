import pytest

from flag_engine.identities.schemas import TraitSchema


@pytest.mark.parametrize(
    "trait_data",
    (
        {"trait_key": "key", "trait_value": "value"},
        {"trait_key": "key1", "trait_value": 21},
        {"trait_key": "key1", "trait_value": None},
        {"trait_key": "key1", "trait_value": 11.2},
        {"trait_key": "key1", "trait_value": True},
    ),
)
def test_trait_schema_load_and_dump(trait_data):
    # Given
    trait_schema = TraitSchema()

    # Then
    loaded_trait_data = trait_schema.load(trait_data)

    assert trait_data == trait_schema.dump(loaded_trait_data)
