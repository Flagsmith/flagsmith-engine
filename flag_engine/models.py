from dataclasses import dataclass

import typing


@dataclass
class Feature:
    id: int
    name: str


@dataclass
class FeatureState:
    id: int
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
    segments: typing.List[Segment]


@dataclass
class Environment:
    id: int
    api_key: str
    project: Project
    feature_states: typing.List[FeatureState] = None


@dataclass
class Trait:
    trait_key: str
    trait_value: typing.Any


@dataclass
class Identity:
    id: int
    identifier: str
    environment: Environment
    feature_states: typing.List[FeatureState]
    traits = typing.List[Trait]
