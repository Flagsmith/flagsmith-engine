import typing

from marshmallow import fields


class DjangoRelatedManagerField(fields.List):
    def __init__(self, *args, filter_func: typing.Callable = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_func = filter_func

    def _serialize(
        self, value, *args, **kwargs
    ) -> typing.Optional[typing.List[typing.Any]]:
        # indicates that the object was passed from django and the 'list' is
        # actually a related manager field, so grab all of the related objects
        # and filter them as necessary (this is done outside of the django ORM to
        # allow for prefetch related optimisations).
        value = list(value.all())
        if self.filter_func:
            value = list(filter(self.filter_func, value))
        return super(DjangoRelatedManagerField, self)._serialize(value, *args, **kwargs)
