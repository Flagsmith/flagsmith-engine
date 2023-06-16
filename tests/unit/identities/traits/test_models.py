import pytest
from pydantic import ValidationError

from flag_engine.identities.traits import models


def test_trait_model__invalid_trait_value__raises_expected():
    # Given
    invalid_trait_kwargs = {"trait_key": "scream", "trait_value": "A" * 2001}

    # When
    with pytest.raises(ValidationError) as exc_info:
        models.TraitModel(**invalid_trait_kwargs)

    # Then
    assert (
        exc_info.value.errors()[-1]["msg"]
        == "ensure this value has at most 2000 characters"
    )
