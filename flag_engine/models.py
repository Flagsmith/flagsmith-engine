from dataclasses import dataclass, field

import typing

from flag_engine import constants
from flag_engine.utils import get_hashed_percentage_for_object_ids


@dataclass
class Feature:
    id: int
    name: str

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


@dataclass
class FeatureState:
    feature: Feature
    enabled: bool
    value: typing.Any = None


@dataclass
class SegmentCondition:
    operator: str
    value: typing.Any
    property_: str = None

    def matches_trait_value(self, trait_value: typing.Any) -> bool:
        matching_function_name = {
            constants.EQUAL: "__eq__",
            constants.GREATER_THAN: "__gt__",
            constants.GREATER_THAN_INCLUSIVE: "__ge__",
            constants.LESS_THAN: "__lt__",
            constants.LESS_THAN_INCLUSIVE: "__le__",
            constants.NOT_EQUAL: "__ne__",
            constants.CONTAINS: "__contains__",
            constants.NOT_CONTAINS: "__contains__",
        }.get(self.operator)

        matching_function = getattr(
            trait_value, matching_function_name, lambda v: False
        )
        result = matching_function(self.value)

        if self.operator == constants.NOT_CONTAINS:
            # negate the contains result as there is no built in method for notcontains
            return not result

        return result


@dataclass
class SegmentRule:
    type: str
    rules: typing.List["SegmentRule"] = field(default_factory=list)
    conditions: typing.List[SegmentCondition] = field(default_factory=list)

    @staticmethod
    def none(iterable: typing.Iterable) -> bool:
        return not any(iterable)

    @property
    def matching_function(self) -> callable:
        return {
            constants.ANY_RULE: any,
            constants.ALL_RULE: all,
            constants.NONE_RULE: SegmentRule.none,
        }.get(self.type)


@dataclass
class Segment:
    id: int
    name: str
    rules: typing.List[SegmentRule]


@dataclass
class SegmentOverride:
    segment: Segment
    feature_state: FeatureState


@dataclass
class Project:
    id: int
    name: str
    segments: typing.List[Segment] = field(default_factory=list)


@dataclass
class Environment:
    id: int
    api_key: str
    project: Project
    feature_states: typing.List[FeatureState] = field(default_factory=list)
    segment_overrides: typing.List[SegmentOverride] = field(default_factory=list)

    def get_feature_state_for_feature(self, feature: Feature) -> FeatureState:
        return next(filter(lambda fs: fs.feature == feature, self.feature_states))


@dataclass
class Trait:
    trait_key: str
    trait_value: typing.Any


@dataclass
class Identity:
    id: int
    identifier: str
    environment_id: int
    feature_states: typing.List[FeatureState] = None
    traits: typing.List[Trait] = None

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
        return any(
            self.matches_segment_rule(rule=rule, segment_id=segment.id)
            for rule in segment.rules
        )

    def matches_segment_rule(self, rule: SegmentRule, segment_id: int) -> bool:
        if rule.rules:
            return rule.matching_function(
                [self.matches_segment_rule(nested, segment_id) for nested in rule.rules]
            )

        return rule.matching_function(
            [
                self.matches_segment_condition(condition, segment_id)
                for condition in rule.conditions
            ]
        )

    def matches_segment_condition(
        self, condition: SegmentCondition, segment_id: int
    ) -> bool:
        if condition.operator == constants.PERCENTAGE_SPLIT:
            normalised_value = condition.value / 100
            return (
                get_hashed_percentage_for_object_ids([segment_id, self.id])
                <= normalised_value
            )

        trait = next(filter(lambda t: t.trait_key == condition.property_, self.traits))
        return condition.matches_trait_value(trait.trait_value) if trait else False
