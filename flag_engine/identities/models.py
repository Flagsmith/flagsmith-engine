import typing
from dataclasses import dataclass, field

from flag_engine.segments import constants
from flag_engine.environments.models import Environment
from flag_engine.features.models import FeatureState
from flag_engine.segments.models import Segment, SegmentRule, SegmentCondition
from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids


@dataclass
class Trait:
    trait_key: str
    trait_value: typing.Any


@dataclass
class Identity:
    id: int
    identifier: str
    environment_id: int
    feature_states: typing.List[FeatureState] = field(default_factory=list)
    traits: typing.List[Trait] = field(default_factory=list)

    def get_all_feature_states(
        self, environment: Environment
    ) -> typing.List[FeatureState]:
        all_feature_states = {fs.feature: fs for fs in environment.feature_states}

        # TODO:
        #  - multivariate

        for segment_override in environment.segment_overrides:
            feature_state = segment_override.feature_state
            feature = feature_state.feature
            if self.in_segment(segment_override.segment):
                all_feature_states[feature] = feature_state

        for feature_state in self.feature_states:
            if feature_state.feature in all_feature_states:
                all_feature_states[feature_state.feature] = feature_state

        return list(all_feature_states.values())

    def in_segment(self, segment: Segment) -> bool:
        return len(segment.rules) > 0 and all(
            self._matches_segment_rule(rule=rule, segment_id=segment.id)
            for rule in segment.rules
        )

    def _matches_segment_rule(self, rule: SegmentRule, segment_id: int) -> bool:
        if rule.rules:
            return rule.matching_function(
                [
                    self._matches_segment_rule(nested, segment_id)
                    for nested in rule.rules
                ]
            )

        return rule.matching_function(
            [
                self._matches_segment_condition(condition, segment_id)
                for condition in rule.conditions
            ]
        )

    def _matches_segment_condition(
        self, condition: SegmentCondition, segment_id: int
    ) -> bool:
        if condition.operator == constants.PERCENTAGE_SPLIT:
            normalised_value = condition.value / 100
            return (
                get_hashed_percentage_for_object_ids([segment_id, self.id])
                <= normalised_value
            )

        trait = next(
            filter(lambda t: t.trait_key == condition.property_, self.traits), None
        )
        return condition.matches_trait_value(trait.trait_value) if trait else False
