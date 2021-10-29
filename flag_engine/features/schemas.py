import typing

from marshmallow import Schema, fields, post_load, validate

from flag_engine.features.models import (
    FeatureModel,
    FeatureStateModel,
    MultivariateFeatureOptionModel,
    MultivariateFeatureStateValueModel,
)
from flag_engine.utils.marshmallow.fields import ListOrDjangoRelatedManagerField
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class FeatureSchema(LoadToModelSchema):
    id = fields.Int()
    name = fields.Str()
    type = fields.Str()

    class Meta:
        model_class = FeatureModel


class MultivariateFeatureOptionSchema(LoadToModelSchema):
    value = fields.Field(allow_none=True)

    class Meta:
        model_class = MultivariateFeatureOptionModel


class MultivariateFeatureStateValueSchema(LoadToModelSchema):
    id = fields.Int()
    multivariate_feature_option = fields.Nested(MultivariateFeatureOptionSchema)
    percentage_allocation = fields.Decimal(validate=[validate.Range(0, 100)])

    class Meta:
        model_class = MultivariateFeatureStateValueModel


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
    multivariate_feature_state_values = ListOrDjangoRelatedManagerField(
        fields.Nested(MultivariateFeatureStateValueSchema)
    )

    @post_load()
    def make_feature_state(self, data, **kwargs) -> FeatureStateModel:
        value = data.pop("value", None)
        feature_state = FeatureStateModel(**data)
        feature_state.set_value(value)
        return feature_state

    def serialize_value(self, instance: object) -> typing.Any:
        if isinstance(instance, dict) and "value" in instance:
            return instance["value"]

        getter = getattr(instance, "get_feature_state_value", lambda *args: None)
        return getter()

    def deserialize_value(self, value: typing.Any) -> typing.Any:
        return value
