import uuid

from marshmallow import EXCLUDE, Schema, fields, post_dump, post_load, validate

from flag_engine.features.models import (
    FeatureModel,
    FeatureSegmentModel,
    FeatureStateModel,
    MultivariateFeatureOptionModel,
    MultivariateFeatureStateValueModel,
)
from flag_engine.utils.exceptions import InvalidPercentageAllocation
from flag_engine.utils.marshmallow.schemas import LoadToModelSchema


class FeatureSegmentSchema(LoadToModelSchema):
    priority = fields.Int()

    class Meta:
        model_class = FeatureSegmentModel


class FeatureSchema(LoadToModelSchema):
    id = fields.Int()
    name = fields.Str()
    type = fields.Str()

    class Meta:
        model_class = FeatureModel


class MultivariateFeatureOptionSchema(LoadToModelSchema):
    id = fields.Int(allow_none=True)
    value = fields.Field(allow_none=True)

    class Meta:
        model_class = MultivariateFeatureOptionModel


class MultivariateFeatureStateValueSchema(LoadToModelSchema):
    id = fields.Int(allow_none=True)
    mv_fs_value_uuid = fields.Str(dump_default=uuid.uuid4)
    multivariate_feature_option = fields.Nested(MultivariateFeatureOptionSchema)
    percentage_allocation = fields.Decimal(validate=[validate.Range(0, 100)])

    class Meta:
        model_class = MultivariateFeatureStateValueModel


class BaseFeatureStateSchema(Schema):
    featurestate_uuid = fields.Str(dump_default=uuid.uuid4)
    feature = fields.Nested(FeatureSchema)
    enabled = fields.Bool()
    # Used for storing feature segment priority
    feature_segment = fields.Nested(FeatureSegmentSchema, allow_none=True)

    class Meta:
        unknown = EXCLUDE


class FeatureStateSchema(BaseFeatureStateSchema):
    feature_state_value = fields.Field(allow_none=True, required=False)
    multivariate_feature_state_values = fields.List(
        fields.Nested(MultivariateFeatureStateValueSchema)
    )
    django_id = fields.Int(allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load()
    def make_feature_state(self, data, **kwargs) -> FeatureStateModel:
        value = data.pop("feature_state_value", None)
        feature_state = FeatureStateModel(**data)
        feature_state.set_value(value)
        return feature_state

    @post_dump()
    def validate_percentage_allocations(self, data, **kwargs):
        """Since we do support modifying percentage allocation on a per identity override bases
        we need to validate the percentage before building the document(dict)"""
        # Since client(s) can exclude this field from dumping we need to make sure
        # We only run the validation if the field is present on the serializer
        if "multivariate_feature_state_values" not in self.fields:
            return data

        total_allocation = sum(
            mvfsv["percentage_allocation"]
            for mvfsv in data["multivariate_feature_state_values"]
        )
        if total_allocation > 100:

            raise InvalidPercentageAllocation(
                "Total percentage allocation should not be more than 100"
            )
        return data
