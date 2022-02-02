import typing

from marshmallow import fields, post_dump, pre_dump

from flag_engine.django_transform.fields import DjangoRelatedManagerField
from flag_engine.django_transform.filters import sort_and_filter_feature_segments
from flag_engine.environments.schemas import (
    BaseEnvironmentAPIKeySchema,
    BaseEnvironmentSchema,
)
from flag_engine.features.schemas import (
    BaseFeatureStateSchema,
    MultivariateFeatureStateValueSchema,
)
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.schemas import BaseIdentitySchema
from flag_engine.identities.traits.schemas import TraitSchema
from flag_engine.projects.schemas import BaseProjectSchema
from flag_engine.segments.schemas import (
    BaseSegmentConditionSchema,
    BaseSegmentRuleSchema,
    BaseSegmentSchema,
)


class DjangoFeatureStateSchema(BaseFeatureStateSchema):
    feature_state_value = fields.Method(serialize="serialize_feature_state_value")
    multivariate_feature_state_values = DjangoRelatedManagerField(
        fields.Nested(MultivariateFeatureStateValueSchema), dump_only=True
    )

    django_id = fields.Int(attribute="id")

    def serialize_feature_state_value(self, instance) -> typing.Any:
        return instance.get_feature_state_value()


class DjangoSegmentConditionSchema(BaseSegmentConditionSchema):
    property_ = fields.Str(attribute="property", dump_only=True)


class DjangoSegmentRuleSchema(BaseSegmentRuleSchema):
    rules = DjangoRelatedManagerField(
        fields.Nested("DjangoSegmentRuleSchema"), required=False, dump_only=True
    )
    conditions = DjangoRelatedManagerField(
        fields.Nested(DjangoSegmentConditionSchema), required=False, dump_only=True
    )


class DjangoSegmentSchema(BaseSegmentSchema):
    rules = DjangoRelatedManagerField(
        fields.Nested(DjangoSegmentRuleSchema), dump_only=True
    )
    feature_states = fields.Method(serialize="serialize_feature_states")

    def __init__(self, *args, **kwargs):
        super(DjangoSegmentSchema, self).__init__(*args, **kwargs)
        self.feature_state_schema = DjangoFeatureStateSchema()

    def serialize_feature_states(self, instance: typing.Any) -> typing.List[dict]:
        # api key is set in the context using a pre_dump method on EnvironmentSchema.
        environment_api_key = self.context.get("environment_api_key")
        feature_segments = sort_and_filter_feature_segments(
            instance.feature_segments.all(), environment_api_key
        )

        # Django datamodel incorrectly uses a foreign key for the
        # FeatureState -> FeatureSegment relationship so we have to recursively
        # build the list like this
        feature_states = []
        for feature_segment in feature_segments:
            feature_states.extend(feature_segment.feature_states.all())
        return self.feature_state_schema.dump(feature_states, many=True)


class DjangoIdentitySchema(BaseIdentitySchema):
    identity_traits = DjangoRelatedManagerField(
        fields.Nested(TraitSchema), required=False
    )
    identity_features = DjangoRelatedManagerField(
        fields.Nested(DjangoFeatureStateSchema), required=False
    )
    django_id = fields.Int(attribute="id")
    environment_api_key = fields.Method(serialize="serialize_environment_api_key")

    @post_dump
    def generate_composite_key(self, data: typing.Dict[str, typing.Any], **kwargs):
        data.setdefault(
            "composite_key",
            IdentityModel.generate_composite_key(
                env_key=data["environment_api_key"], identifier=data["identifier"]
            ),
        )
        return data

    def serialize_environment_api_key(self, instance: typing.Any) -> str:
        return instance.environment.api_key


class DjangoProjectSchema(BaseProjectSchema):
    segments = DjangoRelatedManagerField(
        fields.Nested(DjangoSegmentSchema), required=False, dump_only=True
    )


class DjangoEnvironmentSchema(BaseEnvironmentSchema):
    feature_states = DjangoRelatedManagerField(
        fields.Nested(DjangoFeatureStateSchema),
        filter_func=lambda e: e.feature_segment_id is None and e.identity_id is None,
        dump_only=True,
    )
    project = fields.Nested(DjangoProjectSchema, dump_only=True)

    @pre_dump()
    def set_environment_key_in_context(self, obj, *args, **kwargs):
        self.context["environment_api_key"] = getattr(obj, "api_key", None)
        return obj


class DjangoEnvironmentAPIKeySchema(BaseEnvironmentAPIKeySchema):
    client_api_key = fields.Method(serialize="serialize_client_api_key")

    def serialize_client_api_key(self, instance: typing.Any) -> str:
        return instance.environment.api_key
