from typing import Union

from pydantic.types import confloat, constr

from flag_engine.identities.traits.constants import TRAIT_STRING_VALUE_MAX_LENGTH

TraitValue = Union[
    None,
    confloat(allow_inf_nan=False),
    int,
    bool,
    constr(max_length=TRAIT_STRING_VALUE_MAX_LENGTH),
]
