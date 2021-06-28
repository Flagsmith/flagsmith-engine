from dataclasses import dataclass

import typing


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
    rules: typing.List["SegmentRule"] = None
    conditions: typing.List[SegmentCondition] = None


@dataclass
class Segment:
    id: int
    name: str
    rules: typing.List[SegmentRule]


@dataclass
class Project:
    id: int
    name: str
    segments: typing.List[Segment] = None


@dataclass
class Environment:
    id: int
    api_key: str
    project: Project
    feature_states: typing.List[FeatureState] = None

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

        # TODO: segments

        for feature_state in self.feature_states:
            if feature_state.feature in all_feature_states:
                all_feature_states[feature_state.feature] = feature_state

        return list(all_feature_states.values())
