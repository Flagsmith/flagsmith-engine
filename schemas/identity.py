from marshmallow import Schema, fields, post_load
from models.identity import Identity

from datetime import date
from pprint import pprint

class TraitSchema(Schema):
    key = fields.Str()
    value = fields.Str()


class IdentityFlagSchema(Schema):
    name = fields.Str()


class IdentitySchema(Schema):
    identifier = fields.Str()
    created_date = fields.Date()
    environment_id = fields.Integer()
    environment_api_key = fields.Str()
    traits = fields.List(fields.Nested(TraitSchema))
    identity_flags = fields.List(fields.Nested(IdentityFlagSchema))

    @post_load
    def make_identity(self, data, **kwargs):
        return Identity(**data)




