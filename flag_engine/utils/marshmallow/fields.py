from marshmallow import fields

from flag_engine.utils.collections import IdentityFeaturesList


class IdentityFeaturesListField(fields.List):
    def _deserialize(self, value, attr, data, **kwargs) -> IdentityFeaturesList:
        return IdentityFeaturesList(super()._deserialize(value, attr, data, **kwargs))
