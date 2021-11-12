import datetime
import typing
from dataclasses import dataclass, field

from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)
from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids

from .context_managers import override_identity_traits


@dataclass
class TraitModel:
    trait_key: str
    trait_value: typing.Any


def _get_env_feature_states_dict(
    environment: EnvironmentModel,
    feature_name: str = None,
) -> typing.Dict[FeatureModel, FeatureStateModel]:
    feature_states = environment.feature_states
    if feature_name:
        feature_states = [environment.get_feature_state(feature_name)]
    return {fs.feature: fs for fs in feature_states}


@dataclass
class IdentityModel:
    identifier: str
    environment_api_key: str
    created_date: datetime = field(default_factory=datetime.datetime.now)
    identity_features: typing.List[FeatureStateModel] = field(default_factory=list)
    identity_traits: typing.List[TraitModel] = field(default_factory=list)

    @property
    def composite_key(self):
        return self.generate_composite_key(self.environment_api_key, self.identifier)

    def _get_all_feature_state_dict_with_segment_override(
        self,
        environment,
        feature_name: str = None,
    ) -> None:

        all_feature_states = _get_env_feature_states_dict(environment, feature_name)
        for feature_state in environment.segment_overrides:
            segment = environment.get_segment(feature_state.segment_id)
            if feature_state.feature in all_feature_states and self.in_segment(segment):
                all_feature_states[feature_state.feature] = feature_state
        return all_feature_states

    def get_all_feature_states(
        self,
        environment: EnvironmentModel,
        *,
        traits: typing.List[TraitModel] = None,
        feature_name: str = None,
    ) -> typing.List[FeatureStateModel]:
        with override_identity_traits(self, traits or self.identity_traits):
            # Get feature states with segment override
            feature_states = self._get_all_feature_state_dict_with_segment_override(
                environment, feature_name
            )
            # Override feature states with identity feature states
            feature_states.update(
                {
                    fs.feature: fs
                    for fs in self.identity_features
                    if fs.feature in feature_states
                }
            )
        return list(feature_states.values())

    def in_segment(self, segment: SegmentModel) -> bool:
        return len(segment.rules) > 0 and all(
            self._matches_segment_rule(rule=rule, segment_id=segment.id)
            for rule in segment.rules
        )

    @staticmethod
    def generate_composite_key(env_key: str, identifier: str) -> str:
        return f"{env_key}_{identifier}"

    def _matches_segment_rule(self, rule: SegmentRuleModel, segment_id: int) -> bool:
        matches_conditions = (
            rule.matching_function(
                [
                    self._matches_segment_condition(condition, segment_id)
                    for condition in rule.conditions
                ]
            )
            if len(rule.conditions) > 0
            else True
        )

        return matches_conditions and all(
            [self._matches_segment_rule(rule, segment_id) for rule in rule.rules]
        )

    def _matches_segment_condition(
        self, condition: SegmentConditionModel, segment_id: int
    ) -> bool:
        if condition.operator == constants.PERCENTAGE_SPLIT:
            return (
                get_hashed_percentage_for_object_ids([segment_id, self.id])
                <= condition.value
            )

        # TODO: regex
        trait = next(
            filter(lambda t: t.trait_key == condition.property_, self.identity_traits),
            None,
        )
        return condition.matches_trait_value(trait.trait_value) if trait else False
