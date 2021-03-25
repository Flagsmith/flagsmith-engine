from marshmallow import Schema, fields, post_load, validates_schema, ValidationError

from flag_engine.models import Project, Environment, Trait, Identity, Segment


class FeatureSchema(Schema):
    name = fields.Str()


class FeatureStateSchema(Schema):
    feature = fields.Nested(FeatureSchema)


class SegmentConditionSchema(Schema):
    operator = fields.Str()
    property = fields.Str()
    value = fields.Field()


class SegmentRuleSchema(Schema):
    type = fields.Str()
    rules = fields.List(fields.Nested("SegmentRuleSchema"), required=False)
    conditions = fields.List(fields.Nested(SegmentConditionSchema), required=False)

    @validates_schema()
    def validate_not_rules_and_conditions(self, data, **kwargs):
        if data.get("rules") and data.get("conditions"):
            raise ValidationError(
                "Segment rule must not have both rules and conditions"
            )


class SegmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    rules = fields.List(fields.Nested(SegmentRuleSchema))

    @post_load()
    def make_segment(self, data, **kwargs):
        return Segment(**data)


class ProjectSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    segments = fields.List(fields.Nested(SegmentSchema), required=False)

    @post_load()
    def make_project(self, data, **kwargs) -> Project:
        return Project(**data)


class EnvironmentSchema(Schema):
    id = fields.Int()
    api_key = fields.Str()
    feature_states = fields.List(fields.Nested(FeatureStateSchema))
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
