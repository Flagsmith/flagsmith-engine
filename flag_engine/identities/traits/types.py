from typing import Union

from pydantic.types import AllowInfNan, StringConstraints
from typing_extensions import Annotated

from flag_engine.identities.traits.constants import TRAIT_STRING_VALUE_MAX_LENGTH

TraitValue = Union[
    None,
    bool,
    Annotated[float, AllowInfNan(False)],
    int,
    Annotated[str, StringConstraints(max_length=TRAIT_STRING_VALUE_MAX_LENGTH)],
]
