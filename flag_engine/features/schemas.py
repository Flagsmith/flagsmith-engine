from marshmallow import EXCLUDE, Schema, fields, post_load, validate

from flag_engine.features.models import (
    FeatureModel,
    FeatureStateModel,
    MultivariateFeatureOptionModel,
    MultivariateFeatureStateValueModel,
)
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


class BaseFeatureStateSchema(Schema):
    id = fields.Int()
    feature = fields.Nested(FeatureSchema)
    enabled = fields.Bool()


class FeatureStateSchema(BaseFeatureStateSchema):
    feature_state_value = fields.Field(allow_none=True, required=False)
    multivariate_feature_state_values = fields.List(
        fields.Nested(MultivariateFeatureStateValueSchema)
    )

    class Meta:
        unknown = EXCLUDE

    @post_load()
    def make_feature_state(self, data, **kwargs) -> FeatureStateModel:
        value = data.pop("feature_state_value", None)
        feature_state = FeatureStateModel(**data)
        feature_state.set_value(value)
        return feature_state
