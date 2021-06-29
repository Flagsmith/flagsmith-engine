from marshmallow import (
    Schema,
    fields,
    post_load,
    validates_schema,
    ValidationError,
    validate,
)

from . import constants
from .fields import ListOrDjangoRelatedManagerField
from .models import (
    Project,
    Environment,
    Trait,
    Identity,
    Segment,
    Feature,
    FeatureState,
)


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


class SegmentConditionSchema(Schema):
    operator = fields.Str(validate=validate.OneOf(constants.CONDITION_OPERATORS))
    property_ = fields.Str(data_key="property")
    value = fields.Field()


class SegmentRuleSchema(Schema):
    type = fields.Str(validate=validate.OneOf(constants.RULE_TYPES))
    rules = ListOrDjangoRelatedManagerField(
        fields.Nested("SegmentRuleSchema"), required=False
    )
    conditions = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentConditionSchema), required=False
    )

    @validates_schema()
    def validate_not_rules_and_conditions(self, data, **kwargs):
        if data.get("rules") and data.get("conditions"):
            raise ValidationError(
                "Segment rule must not have both rules and conditions"
            )


class SegmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    rules = ListOrDjangoRelatedManagerField(fields.Nested(SegmentRuleSchema))

    @post_load()
    def make_segment(self, data, **kwargs):
        return Segment(**data)


class ProjectSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    segments = ListOrDjangoRelatedManagerField(
        fields.Nested(SegmentSchema), required=False
    )

    @post_load()
    def make_project(self, data, **kwargs) -> Project:
        return Project(**data)


class EnvironmentSchema(Schema):
    id = fields.Int()
    api_key = fields.Str()
    feature_states = ListOrDjangoRelatedManagerField(fields.Nested(FeatureStateSchema))
    project = fields.Nested(ProjectSchema)

    @post_load()
    def make_environment(self, data: dict, **kwargs) -> Environment:
        return Environment(**data)


class TraitSchema(Schema):
    key = fields.Str()
    value = fields.Str()

    @post_load
    def make_trait(self, data, **kwargs):
        return Trait(**data)


class IdentitySchema(Schema):
    identifier = fields.Str()
    created_date = fields.Date()
    environment_id = fields.Integer()
    environment_api_key = fields.Str()
    traits = fields.List(fields.Nested(TraitSchema))
    identity_flags = fields.List(fields.Nested(FeatureStateSchema))

    @post_load
    def make_identity(self, data, **kwargs):
        return Identity(**data)
