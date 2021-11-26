import pytest

from flag_engine.identities.models import TraitModel
from flag_engine.identities.schemas import TraitSchema


@pytest.mark.parametrize(
    "trait_key,trait_value",
    (
        ("key", "value"),
        ("key1", 21),
        ("key1", None),
        ("key1", 11.2),
        ("key1", True),
    ),
)
def test_trait_schema_load(trait_key, trait_value):
    # Given
    trait_schema = TraitSchema()

    # When
    trait_model = trait_schema.load(
        {"trait_key": trait_key, "trait_value": trait_value}
    )

    # Then
    assert trait_model.trait_key == trait_key
    assert trait_model.trait_value == trait_value


@pytest.mark.parametrize(
    "trait_model",
    (
        TraitModel("key", "value"),
        TraitModel("key", 21),
        TraitModel("key1", None),
        TraitModel("key1", 11.2),
        TraitModel("key1", True),
    ),
)
def test_trait_schema_dump(trait_model):
    # Given
    trait_schema = TraitSchema()

    # When
    trait_data = trait_schema.dump(trait_model)

    # Then
    assert trait_data["trait_key"] == trait_model.trait_key
    assert trait_data["trait_value"] == trait_model.trait_value
