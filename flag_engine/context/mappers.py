import typing

from flag_engine.context.types import EvaluationContext
from flag_engine.environments.models import EnvironmentModel
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel


def map_environment_identity_to_context(
    environment: EnvironmentModel,
    identity: IdentityModel,
    override_traits: typing.Optional[typing.List[TraitModel]],
) -> EvaluationContext:
    """
    Maps an EnvironmentModel and IdentityModel to an EvaluationContext.

    :param environment: The environment model object.
    :param identity: The identity model object.
    :param override_traits: A list of TraitModel objects, to be used in place of `identity.identity_traits` if provided.
    :return: An EvaluationContext containing the environment and identity.
    """
    return {
        "environment": {
            "key": environment.api_key,
            "name": environment.name or "",
        },
        "identity": {
            "identifier": identity.identifier,
            "key": str(identity.django_id or identity.composite_key),
            "traits": {
                trait.trait_key: trait.trait_value
                for trait in (
                    override_traits
                    if override_traits is not None
                    else identity.identity_traits
                )
            },
        },
    }
