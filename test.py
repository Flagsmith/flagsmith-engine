from marshmallow import Schema, fields
from datetime import date
from pprint import pprint

from schemas.identity import IdentitySchema

trait_a = dict(key="email", value="someone@example.com")
trait_b = dict(key="age", value="old lol")
trait_list = [trait_a, trait_b]

benr = dict(identifier="someone@example.com", 
        created_date=date(2020, 1, 1),
        environment_id = 1213, 
        environment_api_key="324234234", 
        traits = trait_list)

idschema = IdentitySchema()
data = idschema.dump(benr)
pprint(data)

identity = idschema.load(data)
pprint(identity)

"""
❯ python identity.py
{ 'created_date': '2020-01-01',
  'environment_api_key': '324234234',
  'environment_id': 1213,
  'identifier': 'someone@example.com',
  'traits': [ {'key': 'email', 'value': 'someone@example.com'},
              {'key': 'age', 'value': 'old lol'}]}
"""