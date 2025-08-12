import operator
import re
import typing
from contextlib import suppress
from functools import partial, wraps

import semver

from flag_engine.context.mappers import map_environment_identity_to_context
from flag_engine.context.types import (
    EvaluationContext,
    FeatureContext,
    SegmentCondition,
    SegmentContext,
    SegmentRule,
)
from flag_engine.environments.models import EnvironmentModel
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.types import ContextValue
from flag_engine.result.types import EvaluationResult, FlagResult, SegmentResult
from flag_engine.segments import constants
from flag_engine.segments.models import SegmentModel
from flag_engine.segments.types import ConditionOperator
from flag_engine.segments.utils import get_matching_function
from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids
from flag_engine.utils.semver import is_semver
from flag_engine.utils.types import SupportsStr, get_casting_function


def get_identity_segments(
    identity: IdentityModel,
    environment: EnvironmentModel,
) -> typing.List[SegmentModel]:
    """
    Get a list of segments for a given identity in a given environment.

    :param identity: the identity model object to get the segments for
    :param environment: the environment model object the identity belongs to
    :return: list of segments that the identity belongs to in the environment
    """
    context = map_environment_identity_to_context(
        environment=environment,
        identity=identity,
        override_traits=None,
    )
    return [
        SegmentModel(id=segment_context["key"], name=segment_context["name"])
        for segment_context in get_context_segments(context)
    ]


def get_context_segments(
    context: EvaluationContext,
) -> typing.List[SegmentResult]:
    """
    Get a list of segments for a given evaluation context.

    :param context: the evaluation context
    :return: list of segments that match the context
    """
    return get_evaluation_result(context)["segments"]


def get_evaluation_result(context: EvaluationContext) -> EvaluationResult:
    """
    Get the evaluation result for a given context.

    :param context: the evaluation context
    :return: EvaluationResult containing the context, flags, and segments
    """
    segments = [
        segment_context
        for segment_context in (context.get("segments") or {}).values()
        if is_context_in_segment(context, segment_context)
    ]

    segment_feature_contexts: typing.Dict[SupportsStr, FeatureContext] = {}
    for segment_context in segments:
        if overrides := segment_context.get("overrides"):
            for override_feature_context in overrides:
                feature_key = override_feature_context["feature_key"]
                if (
                    feature_key not in segment_feature_contexts
                    or override_feature_context["priority"]
                    < segment_feature_contexts[feature_key]["priority"]
                ):
                    segment_feature_contexts[feature_key] = override_feature_context

    flags: typing.List[FlagResult] = [
        (
            {
                "enabled": segment_feature_context["enabled"],
                "feature_key": segment_feature_context["feature_key"],
                "name": segment_feature_context["name"],
                "reason": f"TARGETING_MATCH; segment={segment_context['name']}",
                "value": segment_feature_context.get("value"),
            }
            if (
                segment_feature_context := segment_feature_contexts.get(
                    feature_context["feature_key"],
                )
            )
            else get_flag_result_from_feature_context(
                feature_context,
                get_context_value(context, "$.identity.key"),
            )
        )
        for feature_context in (context.get("features") or {}).values()
    ]

    return {
        "context": context,
        "flags": flags,
        "segments": [
            {
                "key": segment_context["key"],
                "name": segment_context["name"],
            }
            for segment_context in segments
        ],
    }


def get_flag_result_from_feature_context(
    feature_context: FeatureContext,
    key: SupportsStr,
) -> FlagResult:
    """
    Get a feature value from the feature context
    for a given key.

    :param feature_context: the feature context
    :param key: the key to get the value for
    :return: the value for the key in the feature context
    """
    if variants := feature_context.get("variants"):
        percentage_value = get_hashed_percentage_for_object_ids(
            [feature_context["key"], key]
        )

        # We expect `variants` to be pre-sorted in order of persistence. This gives us a
        # way to ensure that the same value is returned every time we use the same
        # percentage value.
        start_percentage = 0.0

        for variant in variants:
            limit = variant["weight"] + start_percentage
            if start_percentage <= percentage_value < limit:
                return {
                    "enabled": feature_context["enabled"],
                    "feature_key": feature_context["feature_key"],
                    "name": feature_context["name"],
                    "reason": "SPLIT",
                    "value": variant["value"],
                }

            start_percentage = limit

    return {
        "enabled": feature_context["enabled"],
        "feature_key": feature_context["feature_key"],
        "name": feature_context["name"],
        "reason": "DEFAULT",
        "value": feature_context["value"],
    }


def is_context_in_segment(
    context: EvaluationContext,
    segment_context: SegmentContext,
) -> bool:
    return bool(rules := segment_context["rules"]) and all(
        context_matches_rule(
            context=context, rule=rule, segment_key=segment_context["key"]
        )
        for rule in rules
    )


def context_matches_rule(
    context: EvaluationContext,
    rule: SegmentRule,
    segment_key: SupportsStr,
) -> bool:
    matches_conditions = (
        get_matching_function(rule["type"])(
            [
                context_matches_condition(
                    context=context,
                    condition=condition,
                    segment_key=segment_key,
                )
                for condition in conditions
            ]
        )
        if (conditions := rule.get("conditions"))
        else True
    )

    return matches_conditions and all(
        context_matches_rule(
            context=context,
            rule=rule,
            segment_key=segment_key,
        )
        for rule in rule.get("rules") or []
    )


def context_matches_condition(
    context: EvaluationContext,
    condition: SegmentCondition,
    segment_key: SupportsStr,
) -> bool:
    context_value = (
        get_context_value(context, condition_property)
        if (condition_property := condition.get("property"))
        else None
    )

    if condition["operator"] == constants.PERCENTAGE_SPLIT:
        if context_value is not None:
            object_ids = [segment_key, context_value]
        else:
            object_ids = [segment_key, get_context_value(context, "$.identity.key")]

        float_value = float(condition["value"])
        return get_hashed_percentage_for_object_ids(object_ids) <= float_value

    if condition["operator"] == constants.IS_NOT_SET:
        return context_value is None

    if condition["operator"] == constants.IS_SET:
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
    condition: SegmentCondition,
    context_value: ContextValue,
) -> bool:
    if matcher := MATCHERS_BY_OPERATOR.get(condition["operator"]):
        return matcher(condition["value"], context_value)

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

    if not segment_value:
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
