from marshmallow import Schema, SchemaOpts, post_load


class LoadToModelSchemaOpts(SchemaOpts):
    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.model_class = getattr(meta, "model_class", None)


class LoadToModelSchema(Schema):
    """Base schema class that returns a model instance if model_class option is set
    on Meta class after loading(using post load hook)

    Example usage:

    .. code-block:: python
        @dataclass
        class AModel:
            id: int

        class ASchema(LoadToModelSchema):
            id = fields.Int()

            class Meta:
                model_class = AModel
    """

    OPTIONS_CLASS = LoadToModelSchemaOpts

    @post_load()
    def make_instance(self, data, **kwargs) -> object:
        if not self.opts.model_class:
            return data
        return self.opts.model_class(**data)
