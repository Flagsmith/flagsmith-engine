from marshmallow import Schema, fields
from datetime import date
from pprint import pprint

class Feature(Schema):
    name = fields.Str()


class FeatureState(Schema):
    feature = fields.Nested(Feature)


class EnvironmentSchema(Schema):
    id = fields.Int()
    api_key = fields.Str()
    flags = fields.List(fields.Nested(FeatureState))
    