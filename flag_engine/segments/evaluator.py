import operator
import re
import typing
from contextlib import suppress
from functools import partial, wraps

import semver

from flag_engine.context.types import EvaluationContext
from flag_engine.identities.traits.types import ContextValue
from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.segments.types import ConditionOperator
from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids
from flag_engine.utils.semver import is_semver
from flag_engine.utils.types import SupportsStr, get_casting_function


def get_context_segments(
    context: EvaluationContext,
    segments: typing.List[SegmentModel],
) -> typing.List[SegmentModel]:
    return [
        segment
        for segment in segments
        if is_context_in_segment(
            context=context,
            segment=segment,
        )
    ]


def is_context_in_segment(
    context: EvaluationContext,
    segment: SegmentModel,
) -> bool:
    return bool(rules := segment.rules) and all(
        context_matches_rule(context=context, rule=rule, segment_key=segment.id)
        for rule in rules
    )


def context_matches_rule(
    context: EvaluationContext,
    rule: SegmentRuleModel,
    segment_key: SupportsStr,
) -> bool:
    matches_conditions = (
        rule.matching_function(
            [
                context_matches_condition(
                    context=context,
                    condition=condition,
                    segment_key=segment_key,
                )
                for condition in conditions
            ]
        )
        if (conditions := rule.conditions)
        else True
    )

    return matches_conditions and all(
        context_matches_rule(
            context=context,
            rule=rule,
            segment_key=segment_key,
        )
        for rule in rule.rules
    )


def context_matches_condition(
    context: EvaluationContext,
    condition: SegmentConditionModel,
    segment_key: SupportsStr,
) -> bool:
    context_value = (
        get_context_value(context, condition.property_) if condition.property_ else None
    )

    if condition.operator == constants.PERCENTAGE_SPLIT:
        assert condition.value

        if context_value is not None:
            object_ids = [segment_key, context_value]
        else:
            object_ids = [segment_key, get_context_value(context, "$.identity.key")]

        float_value = float(condition.value)
        return get_hashed_percentage_for_object_ids(object_ids) <= float_value

    if condition.operator == constants.IS_NOT_SET:
        return context_value is None

    if condition.operator == constants.IS_SET:
        return context_value is not None

    return (
        _matches_context_value(condition, context_value)
        if context_value is not None
        else False
    )


def _get_trait(context: EvaluationContext, trait_key: str) -> ContextValue:
    return (
        identity_context["traits"][trait_key]
        if (identity_context := context["identity"])
        else None
    )


def get_context_value(
    context: EvaluationContext,
    property: str,
) -> ContextValue:
    getter = CONTEXT_VALUE_GETTERS_BY_PROPERTY.get(property) or partial(
        _get_trait,
        trait_key=property,
    )
    try:
        return getter(context)
    except KeyError:
        return None


def _matches_context_value(
    condition: SegmentConditionModel,
    context_value: ContextValue,
) -> bool:
    if matcher := MATCHERS_BY_OPERATOR.get(condition.operator):
        return matcher(condition.value, context_value)

    return False


def _evaluate_not_contains(
    segment_value: typing.Optional[str],
    context_value: ContextValue,
) -> bool:
    return isinstance(context_value, str) and str(segment_value) not in context_value


def _evaluate_regex(
    segment_value: typing.Optional[str],
    context_value: ContextValue,
) -> bool:
    return (
        context_value is not None
        and re.compile(str(segment_value)).match(str(context_value)) is not None
    )


def _evaluate_modulo(
    segment_value: typing.Optional[str],
    context_value: ContextValue,
) -> bool:
    if not isinstance(context_value, (int, float)):
        return False

    if segment_value is None:
        return False

    try:
        divisor_part, remainder_part = segment_value.split("|")
        divisor = float(divisor_part)
        remainder = float(remainder_part)
    except ValueError:
        return False

    return context_value % divisor == remainder


def _evaluate_in(
    segment_value: typing.Optional[str], context_value: ContextValue
) -> bool:
    if segment_value:
        if isinstance(context_value, str):
            return context_value in segment_value.split(",")
        if isinstance(context_value, int) and not any(
            context_value is x for x in (False, True)
        ):
            return str(context_value) in segment_value.split(",")
    return False


def _context_value_typed(
    func: typing.Callable[..., bool],
) -> typing.Callable[[typing.Optional[str], ContextValue], bool]:
    @wraps(func)
    def inner(
        segment_value: typing.Optional[str],
        context_value: typing.Union[ContextValue, semver.Version],
    ) -> bool:
        with suppress(TypeError, ValueError):
            if isinstance(context_value, str) and is_semver(segment_value):
                context_value = semver.Version.parse(
                    context_value,
                )
            match_value = get_casting_function(context_value)(segment_value)
            return func(context_value, match_value)
        return False

    return inner


MATCHERS_BY_OPERATOR: typing.Dict[
    ConditionOperator, typing.Callable[[typing.Optional[str], ContextValue], bool]
] = {
    constants.NOT_CONTAINS: _evaluate_not_contains,
    constants.REGEX: _evaluate_regex,
    constants.MODULO: _evaluate_modulo,
    constants.IN: _evaluate_in,
    constants.EQUAL: _context_value_typed(operator.eq),
    constants.GREATER_THAN: _context_value_typed(operator.gt),
    constants.GREATER_THAN_INCLUSIVE: _context_value_typed(operator.ge),
    constants.LESS_THAN: _context_value_typed(operator.lt),
    constants.LESS_THAN_INCLUSIVE: _context_value_typed(operator.le),
    constants.NOT_EQUAL: _context_value_typed(operator.ne),
    constants.CONTAINS: _context_value_typed(operator.contains),
}


CONTEXT_VALUE_GETTERS_BY_PROPERTY = {
    "$.identity.identifier": lambda context: context["identity"]["identifier"],
    "$.identity.key": lambda context: context["identity"]["key"],
    "$.environment.name": lambda context: context["environment"]["name"],
}
