from decimal import Decimal
from typing import Union

import pytest
from pydantic import ValidationError

from flag_engine.identities.traits import models


def test_trait_model__invalid_trait_value__raise_expected() -> None:
    # Given
    invalid_trait_kwargs = {"trait_key": "scream", "trait_value": "A" * 2001}

    # When
    with pytest.raises(ValidationError) as exc_info:
        models.TraitModel(**invalid_trait_kwargs)

    # Then
    assert (
        exc_info.value.errors()[-1]["msg"]
        == "String should have at most 2000 characters"
    )


@pytest.mark.parametrize(
    "trait_value_argument, expected_trait_value",
    [
        (Decimal("1"), 1),
        (Decimal("1.1"), "1.1"),
        ("1", "1"),
        ("1.0", "1.0"),
    ],
)
def test_trait_model__trait_value__coerce_expected(
    trait_value_argument: Union[Decimal, str],
    expected_trait_value: Union[int, float],
) -> None:
    # When
    trait_model = models.TraitModel(
        trait_key="test_trait",
        trait_value=trait_value_argument,
    )

    # Then
    assert type(trait_model.trait_value) is type(expected_trait_value)
    assert trait_model.trait_value == expected_trait_value
