import operator
import re
import typing
from contextlib import suppress
from functools import wraps

import semver

from flag_engine.environments.models import EnvironmentModel
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.identities.traits.types import TraitValue
from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.segments.types import ConditionOperator
from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids
from flag_engine.utils.semver import is_semver
from flag_engine.utils.types import get_casting_function


def get_identity_segments(
    environment: EnvironmentModel,
    identity: IdentityModel,
    override_traits: typing.Optional[typing.List[TraitModel]] = None,
) -> typing.List[SegmentModel]:
    return list(
        filter(
            lambda s: evaluate_identity_in_segment(identity, s, override_traits),
            environment.project.segments,
        )
    )


def evaluate_identity_in_segment(
    identity: IdentityModel,
    segment: SegmentModel,
    override_traits: typing.Optional[typing.List[TraitModel]] = None,
) -> bool:
    """
    Evaluates whether a given identity is in the provided segment.

    :param identity: identity model object to evaluate
    :param segment: segment model object to evaluate
    :param override_traits: pass in a list of traits to use instead of those on the
        identity model itself
    :return: True if the identity is in the segment, False otherwise
    """
    return len(segment.rules) > 0 and all(
        _traits_match_segment_rule(
            override_traits or identity.identity_traits,
            rule,
            segment.id,
            identity.django_id or identity.composite_key,
        )
        for rule in segment.rules
    )


def _traits_match_segment_rule(
    identity_traits: typing.List[TraitModel],
    rule: SegmentRuleModel,
    segment_id: typing.Union[int, str],
    identity_id: typing.Union[int, str],
) -> bool:
    matches_conditions = (
        rule.matching_function(
            [
                _traits_match_segment_condition(
                    identity_traits, condition, segment_id, identity_id
                )
                for condition in rule.conditions
            ]
        )
        if len(rule.conditions) > 0
        else True
    )

    return matches_conditions and all(
        _traits_match_segment_rule(identity_traits, rule, segment_id, identity_id)
        for rule in rule.rules
    )


def _traits_match_segment_condition(
    identity_traits: typing.List[TraitModel],
    condition: SegmentConditionModel,
    segment_id: typing.Union[int, str],
    identity_id: typing.Union[int, str],
) -> bool:
    if condition.operator == constants.PERCENTAGE_SPLIT:
        assert condition.value
        float_value = float(condition.value)
        return (
            get_hashed_percentage_for_object_ids([segment_id, identity_id])
            <= float_value
        )

    trait = next(
        filter(lambda t: t.trait_key == condition.property_, identity_traits), None
    )

    if condition.operator == constants.IS_NOT_SET:
        return trait is None

    if condition.operator == constants.IS_SET:
        return trait is not None

    return _matches_trait_value(condition, trait.trait_value) if trait else False


def _matches_trait_value(
    condition: SegmentConditionModel,
    trait_value: TraitValue,
) -> bool:
    if match_func := MATCH_FUNCS_BY_OPERATOR.get(condition.operator):
        return match_func(condition.value, trait_value)

    return False


def _evaluate_not_contains(
    segment_value: typing.Optional[str],
    trait_value: TraitValue,
) -> bool:
    return isinstance(trait_value, str) and str(segment_value) not in trait_value


def _evaluate_regex(
    segment_value: typing.Optional[str],
    trait_value: TraitValue,
) -> bool:
    return (
        trait_value is not None
        and re.compile(str(segment_value)).match(str(trait_value)) is not None
    )


def _evaluate_modulo(
    segment_value: typing.Optional[str],
    trait_value: TraitValue,
) -> bool:
    if not isinstance(trait_value, (int, float)):
        return False

    if segment_value is None:
        return False

    try:
        divisor_part, remainder_part = segment_value.split("|")
        divisor = float(divisor_part)
        remainder = float(remainder_part)
    except ValueError:
        return False

    return trait_value % divisor == remainder


def _evaluate_in(segment_value: typing.Optional[str], trait_value: TraitValue) -> bool:
    if segment_value:
        if isinstance(trait_value, str):
            return trait_value in segment_value.split(",")
        if isinstance(trait_value, int) and not any(
            trait_value is x for x in (False, True)
        ):
            return str(trait_value) in segment_value.split(",")
    return False


def _trait_value_typed(
    func: typing.Callable[..., bool],
) -> typing.Callable[[typing.Optional[str], TraitValue], bool]:
    @wraps(func)
    def inner(
        segment_value: typing.Optional[str],
        trait_value: TraitValue,
    ) -> bool:
        with suppress(TypeError, ValueError):
            if isinstance(trait_value, str) and is_semver(segment_value):
                trait_value = semver.VersionInfo.parse(
                    trait_value,
                )
            match_value = get_casting_function(trait_value)(segment_value)
            return func(trait_value, match_value)
        return False

    return inner


MATCH_FUNCS_BY_OPERATOR: typing.Dict[
    ConditionOperator, typing.Callable[[typing.Optional[str], TraitValue], bool]
] = {
    constants.NOT_CONTAINS: _evaluate_not_contains,
    constants.REGEX: _evaluate_regex,
    constants.MODULO: _evaluate_modulo,
    constants.IN: _evaluate_in,
    constants.EQUAL: _trait_value_typed(operator.eq),
    constants.GREATER_THAN: _trait_value_typed(operator.gt),
    constants.GREATER_THAN_INCLUSIVE: _trait_value_typed(operator.ge),
    constants.LESS_THAN: _trait_value_typed(operator.lt),
    constants.LESS_THAN_INCLUSIVE: _trait_value_typed(operator.le),
    constants.NOT_EQUAL: _trait_value_typed(operator.ne),
    constants.CONTAINS: _trait_value_typed(operator.contains),
}
