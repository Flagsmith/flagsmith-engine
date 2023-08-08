from typing import Union

from pydantic.types import confloat, constr

from flag_engine.identities.traits.constants import TRAIT_STRING_VALUE_MAX_LENGTH

TraitValue = Union[
    None,
    int,
    confloat(allow_inf_nan=False),
    bool,
    constr(max_length=TRAIT_STRING_VALUE_MAX_LENGTH),
]
