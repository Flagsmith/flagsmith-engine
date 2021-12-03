from marshmallow import Schema, SchemaOpts, post_load


class LoadToModelSchemaOpts(SchemaOpts):
    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.model_class = getattr(meta, "model_class", None)


class LoadToModelMixin:
    """A mixin class,  that returns a model instance (using model_class option set
    on Meta class) after loading(using post load hook)
    Example usage:

    .. code-block:: python
        @dataclass
        class AModel:
            id: int

        class ASchema(LoadToModelSchema, Schema):
            id = fields.Int()

            class Meta:
                model_class = AModel
    """

    OPTIONS_CLASS = LoadToModelSchemaOpts

    @post_load()
    def make_instance(self, data, **kwargs) -> object:
        return self.opts.model_class(**data)


class LoadToModelSchema(LoadToModelMixin, Schema):
    """Base schema class that uses LoadToModelMixin to create schema classes that
    can be loaded to a model"""
