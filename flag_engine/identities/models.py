import typing
from dataclasses import dataclass, field

from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.models import FeatureStateModel
from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids


@dataclass
class TraitModel:
    trait_key: str
    trait_value: typing.Any


@dataclass
class IdentityModel:
    id: int
    identifier: str
    environment_id: int
    identity_features: typing.List[FeatureStateModel] = field(default_factory=list)
    traits: typing.List[TraitModel] = field(default_factory=list)

    def get_all_feature_states(
        self, environment: EnvironmentModel
    ) -> typing.List[FeatureStateModel]:
        all_feature_states = {fs.feature: fs for fs in environment.feature_states}

        for segment_override in environment.segment_overrides:
            feature_state = segment_override.feature_state
            feature = feature_state.feature
            if self.in_segment(segment_override.segment):
                all_feature_states[feature] = feature_state

        for feature_state in self.identity_features:
            if feature_state.feature in all_feature_states:
                all_feature_states[feature_state.feature] = feature_state

        return list(all_feature_states.values())

    def in_segment(self, segment: SegmentModel) -> bool:
        return len(segment.rules) > 0 and all(
            self._matches_segment_rule(rule=rule, segment_id=segment.id)
            for rule in segment.rules
        )

    def _matches_segment_rule(self, rule: SegmentRuleModel, segment_id: int) -> bool:
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
        self, condition: SegmentConditionModel, segment_id: int
    ) -> bool:
        if condition.operator == constants.PERCENTAGE_SPLIT:
            return (
                get_hashed_percentage_for_object_ids([segment_id, self.id])
                <= condition.value
            )

        trait = next(
            filter(lambda t: t.trait_key == condition.property_, self.traits), None
        )
        return condition.matches_trait_value(trait.trait_value) if trait else False
