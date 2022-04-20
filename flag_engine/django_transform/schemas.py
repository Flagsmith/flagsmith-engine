import typing

from marshmallow import fields, post_dump, pre_dump

from flag_engine.django_transform.fields import (
    DjangoFeatureStatesRelatedManagerField,
    DjangoRelatedManagerField,
)
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
from flag_engine.utils.datetime import utcnow_with_tz


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
        # TODO: move this logic to Django so we can optimise queries
        # api key is set in the context using a pre_dump method on EnvironmentSchema.
        environment_api_key = self.context.get("environment_api_key")
        feature_segments = sort_and_filter_feature_segments(
            instance.feature_segments.all(), environment_api_key
        )

        # iterate over the feature segments and related feature states to end up with
        # a list consisting of the latest version feature state for each feature
        feature_states = {}
        now = utcnow_with_tz()
        for feature_segment in feature_segments:
            for feature_state in feature_segment.feature_states.all():
                existing_feature_state = feature_states.get(feature_state.feature_id)
                if not existing_feature_state or (
                    feature_state.version > existing_feature_state.version
                    and feature_state.live_from < now
                ):
                    feature_states[feature_state.feature_id] = feature_state

        return self.feature_state_schema.dump(list(feature_states.values()), many=True)


class DjangoIdentitySchema(BaseIdentitySchema):
    identity_traits = DjangoRelatedManagerField(
        fields.Nested(TraitSchema), required=False
    )
    identity_features = DjangoFeatureStatesRelatedManagerField(
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
    feature_states = DjangoFeatureStatesRelatedManagerField(
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
