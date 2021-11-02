from marshmallow import Schema, SchemaOpts, post_load


class LoadToModelSchemaOpts(SchemaOpts):
    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.model_class = getattr(meta, "model_class", None)


class LoadToModelSchema(Schema):
    """Base schema class that returns a model instance after loading(using post load hook)

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
            raise ValueError("`model_class` attribute is not set in Meta class.")
        return self.opts.model_class(**data)
