from dataclasses import dataclass

from marshmallow import fields

from flag_engine.utils.marshmallow.schema import LoadToModelSchema


@dataclass
class DummyModel:
    id: int


class DummySchema(LoadToModelSchema):
    model_class = DummyModel
    id = fields.Int()


def test_load_schema_to_model():
    # Given
    dummy_schema = DummySchema()

    # When
    response = dummy_schema.load(data={"id": 10})

    # Then
    assert response == DummyModel(id=10)
