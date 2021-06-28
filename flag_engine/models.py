from dataclasses import dataclass, field

import typing

from flag_engine import constants


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
    property: str
    value: typing.Any


@dataclass
class SegmentRule:
    type: str
    rules: typing.List["SegmentRule"] = field(default_factory=list)
    conditions: typing.List[SegmentCondition] = field(default_factory=list)

    @staticmethod
    def none(iterable: typing.Iterable) -> bool:
        return not any(iterable)


@dataclass
class Segment:
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

    @property
    def trait_keys(self) -> typing.Iterable[str]:
        return (trait.trait_key for trait in self.traits)

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
        return any(self.matches_segment_rule(rule=rule) for rule in segment.rules)

    def matches_segment_rule(self, rule: SegmentRule) -> bool:
        matching_function = {
            constants.ANY_RULE: any,
            constants.ALL_RULE: all,
            constants.NONE_RULE: SegmentRule.none,
        }.get(rule.type)

        if rule.rules:
            return matching_function(
                [self.matches_segment_rule(nested) for nested in rule.rules]
            )

        return matching_function(
            [self.matches_segment_condition(condition) for condition in rule.conditions]
        )

    def matches_segment_condition(self, condition: SegmentCondition) -> bool:
        if condition.operator == constants.PERCENTAGE_SPLIT:
            # TODO:
            return True

        matching_function_name = {
            constants.EQUAL: "__eq__",
            constants.GREATER_THAN: "__gt__",
            constants.GREATER_THAN_INCLUSIVE: "__gte__",
            constants.LESS_THAN: "__lt__",
            constants.LESS_THAN_INCLUSIVE: "__lte__",
            constants.NOT_EQUAL: "__ne__",
            constants.CONTAINS: "__contains__",
            constants.NOT_CONTAINS: "__contains__",
        }.get(condition.operator)
        negate_match_result = condition.operator == constants.NOT_CONTAINS
        matching_function = getattr(
            condition.value, matching_function_name, lambda *value: False
        )

        trait = next(filter(lambda t: t.trait_key == condition.property, self.traits))
        if trait:
            result = matching_function(trait.trait_value)
            result = not result if negate_match_result else result
            return result

        return False
