import typing

from marshmallow import Schema, fields, post_load, validate

from flag_engine.features.models import (
    Feature,
    FeatureState,
    MultivariateFeatureOption,
    MultivariateFeatureStateValue,
)


class FeatureSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    type = fields.Str(required=False, allow_none=True)

    @post_load()
    def make_feature(self, data, **kwargs) -> Feature:
        return Feature(**data)


class MultivariateFeatureOptionSchema(Schema):
    value = fields.Field(allow_none=True)

    @post_load()
    def make_multivariate_feature_option(
        self, data, **kwargs
    ) -> MultivariateFeatureOption:
        return MultivariateFeatureOption(**data)


class MultivariateFeatureStateValueSchema(Schema):
    id = fields.Int()
    multivariate_feature_option = fields.Nested(MultivariateFeatureOptionSchema)
    percentage_allocation = fields.Float(validate=[validate.Range(0, 100)])

    @post_load()
    def make_multivariate_feature_state_value(
        self, data, **kwargs
    ) -> MultivariateFeatureStateValue:
        return MultivariateFeatureStateValue(**data)


class FeatureStateSchema(Schema):
    id = fields.Int()
    feature = fields.Nested(FeatureSchema)
    enabled = fields.Bool()
    value = fields.Method(
        serialize="serialize_value",
        deserialize="deserialize_value",
        allow_none=True,
        required=False,
    )
    multivariate_feature_state_values = fields.List(
        fields.Nested(MultivariateFeatureStateValueSchema)
    )

    @post_load()
    def make_feature_state(self, data, **kwargs) -> FeatureState:
        value = data.pop("value", None)
        feature_state = FeatureState(**data)
        feature_state.set_value(value)
        return feature_state

    def serialize_value(self, instance: object) -> typing.Any:
        if isinstance(instance, dict) and "value" in instance:
            return instance["value"]

        getter = getattr(instance, "get_feature_state_value", lambda *args: None)
        return getter()

    def deserialize_value(self, value: typing.Any) -> typing.Any:
        return value
