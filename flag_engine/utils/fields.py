import typing

from marshmallow import fields


class ListOrDjangoRelatedManagerField(fields.List):
    def _serialize(
        self, value, *args, **kwargs
    ) -> typing.Optional[typing.List[typing.Any]]:
        if hasattr(value, "filter"):
            # indicates that the object was passed from django and the 'list' is
            # actually a related manager field, so grab all of the filtered related
            # objects
            filter_kwargs = self.metadata.get("filter_kwargs", {})
            value = list(value.filter(**filter_kwargs))
        return super(ListOrDjangoRelatedManagerField, self)._serialize(
            value, *args, **kwargs
        )
