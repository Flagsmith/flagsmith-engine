from marshmallow import Schema, fields, post_load

from flag_engine.features.models import Feature, FeatureState


class FeatureSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    type = fields.Str(required=False, allow_none=True)

    @post_load()
    def make_feature(self, data, **kwargs) -> Feature:
        return Feature(**data)


class FeatureStateSchema(Schema):
    feature = fields.Nested(FeatureSchema)
    enabled = fields.Bool()
    value = fields.Field(allow_none=True)

    @post_load()
    def make_feature_state(self, data, **kwargs) -> FeatureState:
        return FeatureState(**data)
