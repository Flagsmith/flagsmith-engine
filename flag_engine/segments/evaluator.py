import json
import operator
import re
import typing
import warnings
from contextlib import suppress
from functools import lru_cache, wraps

import jsonpath_rfc9535
import semver

from flag_engine.context.mappers import map_any_value_to_context_value
from flag_engine.context.types import (
    EvaluationContext,
    FeatureContext,
    SegmentCondition,
    SegmentContext,
    SegmentRule,
    StrValueSegmentCondition,
)
from flag_engine.result.types import EvaluationResult, FlagResult, SegmentResult
from flag_engine.segments import constants
from flag_engine.segments.types import ConditionOperator, ContextValue, is_context_value
from flag_engine.segments.utils import escape_double_quotes, get_matching_function
from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids
from flag_engine.utils.semver import is_semver
from flag_engine.utils.types import SupportsStr, get_casting_function


class FeatureContextWithSegmentName(typing.TypedDict):
    feature_context: FeatureContext
    segment_name: str


def get_evaluation_result(context: EvaluationContext) -> EvaluationResult:
    """
    Get the evaluation result for a given context.

    :param context: the evaluation context
    :return: EvaluationResult containing the context, flags, and segments
    """
    segments: list[SegmentResult] = []
    flags: list[FlagResult] = []

    segment_feature_contexts: dict[SupportsStr, FeatureContextWithSegmentName] = {}

    for segment_context in (context.get("segments") or {}).values():
        if not is_context_in_segment(context, segment_context):
            continue

        segments.append(
            {
                "key": segment_context["key"],
                "name": segment_context["name"],
            }
        )

        if overrides := segment_context.get("overrides"):
            for override_feature_context in overrides:
                feature_key = override_feature_context["feature_key"]
                if (
                    feature_key not in segment_feature_contexts
                    or override_feature_context.get(
                        "priority",
                        constants.DEFAULT_PRIORITY,
                    )
                    < (segment_feature_contexts[feature_key]["feature_context"]).get(
                        "priority",
                        constants.DEFAULT_PRIORITY,
                    )
                ):
                    segment_feature_contexts[feature_key] = (
                        FeatureContextWithSegmentName(
                            feature_context=override_feature_context,
                            segment_name=segment_context["name"],
                        )
                    )

    identity_key = (
        identity_context["key"]
        if (identity_context := context.get("identity"))
        else None
    )
    for feature_context in (context.get("features") or {}).values():
        if feature_context_with_segment_name := segment_feature_contexts.get(
            feature_context["feature_key"],
        ):
            feature_context = feature_context_with_segment_name["feature_context"]
            flags.append(
                {
                    "enabled": feature_context["enabled"],
                    "feature_key": feature_context["feature_key"],
                    "name": feature_context["name"],
                    "reason": f"TARGETING_MATCH; segment={feature_context_with_segment_name['segment_name']}",
                    "value": feature_context.get("value"),
                }
            )
            continue
        flags.append(
            get_flag_result_from_feature_context(
                feature_context=feature_context,
                key=identity_key,
            )
        )

    return {
        "context": context,
        "flags": flags,
        "segments": segments,
    }


def get_flag_result_from_feature_context(
    feature_context: FeatureContext,
    key: typing.Optional[SupportsStr],
) -> FlagResult:
    """
    Get a feature value from the feature context
    for a given key.

    :param feature_context: the feature context
    :param key: the key to get the value for
    :return: the value for the key in the feature context
    """
    if key is not None and (variants := feature_context.get("variants")):
        percentage_value = get_hashed_percentage_for_object_ids(
            [feature_context["key"], key]
        )

        # We expect `variants` to be pre-sorted in order of persistence. This gives us a
        # way to ensure that the same value is returned every time we use the same
        # percentage value.
        start_percentage = 0.0

        for variant in variants:
            limit = (weight := variant["weight"]) + start_percentage
            if start_percentage <= percentage_value < limit:
                return {
                    "enabled": feature_context["enabled"],
                    "feature_key": feature_context["feature_key"],
                    "name": feature_context["name"],
                    "reason": f"SPLIT; weight={weight}",
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

    if condition["operator"] == constants.IN:
        if isinstance(segment_value := condition["value"], list):
            in_values = segment_value
        else:
            try:
                in_values = json.loads(segment_value)
                # Only accept JSON lists.
                # Ideally, we should use something like pydantic.TypeAdapter[list[str]],
                # but we aim to ditch the pydantic dependency in the future.
                if not isinstance(in_values, list):
                    raise ValueError
            except ValueError:
                in_values = segment_value.split(",")
        in_values = [str(value) for value in in_values]
        # Guard against comparing boolean values to numeric strings.
        if isinstance(context_value, int) and not (
            context_value is True or context_value is False
        ):
            context_value = str(context_value)
        return context_value in in_values

    condition = typing.cast(StrValueSegmentCondition, condition)

    if condition["operator"] == constants.PERCENTAGE_SPLIT:
        if context_value is not None:
            object_ids = [segment_key, context_value]
        elif identity_context := context.get("identity"):
            object_ids = [segment_key, identity_context["key"]]
        else:
            return False

        try:
            float_value = float(condition["value"])
        except ValueError:
            return False
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


def get_context_value(
    context: EvaluationContext,
    property: str,
) -> ContextValue:
    value = None
    if property.startswith("$."):
        value = _get_context_value_getter(property)(context)
    elif identity_context := context.get("identity"):
        if traits := identity_context.get("traits"):
            value = traits.get(property)
    return map_any_value_to_context_value(value)


def _matches_context_value(
    condition: StrValueSegmentCondition,
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


MATCHERS_BY_OPERATOR: dict[
    ConditionOperator, typing.Callable[[typing.Optional[str], ContextValue], bool]
] = {
    constants.NOT_CONTAINS: _evaluate_not_contains,
    constants.REGEX: _evaluate_regex,
    constants.MODULO: _evaluate_modulo,
    constants.EQUAL: _context_value_typed(operator.eq),
    constants.GREATER_THAN: _context_value_typed(operator.gt),
    constants.GREATER_THAN_INCLUSIVE: _context_value_typed(operator.ge),
    constants.LESS_THAN: _context_value_typed(operator.lt),
    constants.LESS_THAN_INCLUSIVE: _context_value_typed(operator.le),
    constants.NOT_EQUAL: _context_value_typed(operator.ne),
    constants.CONTAINS: _context_value_typed(operator.contains),
}


@lru_cache
def _get_context_value_getter(
    property: str,
) -> typing.Callable[[EvaluationContext], ContextValue]:
    """
    Get a function to retrieve a context value based on property value,
    assumed to be either a JSONPath string or a trait key.

    :param property: The property to retrieve the value for.
    :return: A function that takes an EvaluationContext and returns the value.
    """
    try:
        compiled_query = jsonpath_rfc9535.compile(property)
    except jsonpath_rfc9535.JSONPathSyntaxError:
        # This covers a rare case when a trait starting with "$.",
        # but not a valid JSONPath, is used.
        compiled_query = jsonpath_rfc9535.compile(
            f'$.identity.traits["{escape_double_quotes(property)}"]',
        )

    def getter(context: EvaluationContext) -> ContextValue:
        if typing.TYPE_CHECKING:  # pragma: no cover
            # Ugly hack to satisfy mypy :(
            data = dict(context)
        else:
            data = context
        try:
            if result := compiled_query.find_one(data):
                if is_context_value(value := result.value):
                    return value
            return None
        except jsonpath_rfc9535.JSONPathError:  # pragma: no cover
            # This is supposed to be unreachable, but if it happens,
            # we log a warning and return None.
            warnings.warn(
                f"Failed to evaluate JSONPath query '{property}' in context: {context}",
                RuntimeWarning,
            )
            return None

    return getter
