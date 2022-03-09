import typing

from flag_engine.identities.models import IdentityModel
from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids

from ..environments.models import EnvironmentModel
from ..identities.traits.models import TraitModel
from . import constants
from .models import SegmentConditionModel, SegmentModel, SegmentRuleModel


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
        float_value = float(condition.value)
        return (
            get_hashed_percentage_for_object_ids([segment_id, identity_id])
            <= float_value
        )

    trait = next(
        filter(lambda t: t.trait_key == condition.property_, identity_traits), None
    )
    return condition.matches_trait_value(trait.trait_value) if trait else False
