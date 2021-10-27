from marshmallow import Schema, post_load


class LoadToModelSchema(Schema):
    model_class: object

    @post_load()
    def make_instance(self, data, **kwargs) -> object:
        return self.model_class(**data)
