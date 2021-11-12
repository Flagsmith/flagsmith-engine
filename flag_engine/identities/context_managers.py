import typing
from contextlib import contextmanager


@contextmanager
def override_identity_traits(
    identity_model: "IdentityModel", traits: typing.List["TraitModel"]  # noqa: F821
):
    """
    Used for overriding `identity_traits` attribute of `IdentityModel`
    to support processing traits without having to save them on the `IdentityModel`
    or passing them as additional argument to the function.
    """
    stored_traits = identity_model.identity_traits
    identity_model.identity_traits = traits
    try:
        yield identity_model
    finally:
        identity_model.identity_traits = stored_traits
