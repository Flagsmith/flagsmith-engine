from typing import Union

from pydantic import constr

from flag_engine.identities.traits.constants import TRAIT_STRING_VALUE_MAX_LENGTH

TraitValue = Union[
    None,
    float,
    int,
    bool,
    constr(max_length=TRAIT_STRING_VALUE_MAX_LENGTH),
]
