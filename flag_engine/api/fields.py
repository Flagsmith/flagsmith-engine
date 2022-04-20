import typing

from marshmallow.fields import Field, List

from .constants import ACCEPTED_TRAIT_VALUE_TYPES

from flag_engine.utils.datetime import utcnow_with_tz


class APITraitValueField(Field):
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


class DjangoRelatedManagerField(List):
    def __init__(self, *args, filter_func: typing.Callable = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_func = filter_func

    def get_value(self, obj, attr, **kwargs) -> typing.List[typing.Any]:
        # indicates that the object was passed from django and the 'list' is
        # actually a related manager field, so grab all of the related objects
        # and filter them as necessary (this is done outside of the django ORM to
        # allow for prefetch related optimisations).
        value = list(getattr(obj, attr).all())
        if self.filter_func:
            value = list(filter(self.filter_func, value))
        return value


class DjangoFeatureStatesRelatedManagerField(DjangoRelatedManagerField):
    def get_value(self, obj, attr, **kwargs):
        now = utcnow_with_tz()
        features_map = {}
        for fs in getattr(obj, attr).all():
            if self.filter_func and not self.filter_func(fs):
                continue

            existing_feature_state = features_map.get(fs.feature_id)
            if not existing_feature_state or (
                fs.live_from < now and fs.version > existing_feature_state.version
            ):
                features_map[fs.feature_id] = fs

        return list(features_map.values())
