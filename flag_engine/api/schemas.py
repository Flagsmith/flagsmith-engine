import typing

from marshmallow import ValidationError, validates

from flag_engine.identities.schemas import TraitSchema

from .constants import TRAIT_STRING_VALUE_MAX_LENGTH
from .fields import APITraitValueField


class APITraitSchema(TraitSchema):
    trait_value = APITraitValueField(allow_none=True)

    @validates("trait_value")
    def validate_trait_value_length(
        self, trait_value: typing.Union[int, str, bool, float]
    ):
        type_ = type(trait_value)
        if type_ == str and len(trait_value) > TRAIT_STRING_VALUE_MAX_LENGTH:
            raise ValidationError(
                f"Value string is too long. Must be less than "
                f"{TRAIT_STRING_VALUE_MAX_LENGTH} character"
            )
