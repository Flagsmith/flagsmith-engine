import typing

from marshmallow.fields import Field

from .constants import ACCEPTED_TRAIT_VALUE_TYPES


class APITraitValueField(Field):
    def _serialize(self, value: typing.Any, attr: str, obj: typing.Any, **kwargs):
        return value

    def _deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str],
        data: typing.Optional[typing.Mapping[str, typing.Any]],
        **kwargs,
    ):
        if type(value) not in ACCEPTED_TRAIT_VALUE_TYPES:
            value = str(value)
        return value
