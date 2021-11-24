import typing
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DjangoSegmentCondition:
    operator: str
    property: str
    value: typing.Any


@dataclass
class DjangoSegmentConditionRelatedObjectManager:
    conditions: typing.List[DjangoSegmentCondition]

    def filter(self, **filter_kwargs) -> typing.List[DjangoSegmentCondition]:
        return self.conditions


class DjangoSegmentRule:
    type: str
    rules: "DjangoSegmentRuleRelatedObjectManager" = None
    conditions: DjangoSegmentConditionRelatedObjectManager = field(default_factory=list)

    def __init__(
        self,
        type: str,
        rules: typing.List["DjangoSegmentRule"] = None,
        conditions: typing.List[DjangoSegmentCondition] = None,
    ):
        self.type = type
        self.rules = DjangoSegmentRuleRelatedObjectManager(rules or [])
        self.conditions = DjangoSegmentConditionRelatedObjectManager(conditions or [])


@dataclass
class DjangoSegmentRuleRelatedObjectManager:
    rules: typing.List[DjangoSegmentRule]

    def filter(self, **filter_kwargs) -> typing.List[DjangoSegmentRule]:
        return self.rules

    def all(self) -> typing.List[DjangoSegmentRule]:
        return self.rules


class DjangoSegment:
    def __init__(
        self,
        id: int,
        name: str,
        rules: typing.List[DjangoSegmentRule] = None,
        feature_segments: typing.List["DjangoFeatureSegment"] = None,
    ):
        self.id = id
        self.name = name
        self.rules = DjangoSegmentRuleRelatedObjectManager(rules or [])
        self.feature_segments = DjangoFeatureSegmentRelatedObjectManager(
            feature_segments or []
        )


@dataclass
class DjangoSegmentRelatedObjectManager:
    segments: typing.List[DjangoSegment]

    def filter(self, **filter_kwargs) -> typing.List[DjangoSegment]:
        return self.segments


class DjangoFeatureSegment:
    def __init__(self, feature_states: typing.List["DjangoFeatureState"] = None):
        self.feature_states = DjangoFeatureStateRelatedManager(feature_states or [])


@dataclass
class DjangoFeatureSegmentRelatedObjectManager:
    feature_segments: typing.List[DjangoFeatureSegment]

    def filter(self, **filter_kwargs) -> typing.List[DjangoFeatureSegment]:
        return self.feature_segments

    def all(self) -> typing.List[DjangoFeatureSegment]:
        return self.feature_segments

    def order_by(self, *args) -> "DjangoFeatureSegmentRelatedObjectManager":
        return self


@dataclass
class DjangoOrganisation:
    id: int
    name: str
    stop_serving_flags: bool = False
    persist_trait_data: bool = True
    feature_analytics: bool = True


class DjangoProject:
    def __init__(
        self,
        id: int,
        name: str,
        organisation: DjangoOrganisation,
        hide_disabled_flags: bool = False,
        segments: typing.List[DjangoSegment] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.organisation = organisation
        self.hide_disabled_flags = hide_disabled_flags
        self.segments = DjangoSegmentRelatedObjectManager(segments or [])


@dataclass
class DjangoFeature:
    id: int
    name: str
    project: DjangoProject
    type: str


@dataclass
class DjangoMultivariateFeatureOption:
    value: typing.Any


@dataclass
class DjangoMultivariateFeatureStateValue:
    id: int
    percentage_allocation: float
    multivariate_feature_option: DjangoMultivariateFeatureOption


@dataclass
class DjangoMultivariateFeatureStateValueRelatedManager:
    multivariate_feature_state_values: typing.List[
        DjangoMultivariateFeatureStateValue
    ] = field(default_factory=list)

    def filter(
        self, **filter_kwargs
    ) -> typing.List[DjangoMultivariateFeatureStateValue]:
        return self.multivariate_feature_state_values


class DjangoFeatureState:
    def __init__(
        self,
        id: int,
        feature: DjangoFeature,
        enabled: bool,
        feature_segment: DjangoFeatureSegment = None,
        identity: "DjangoIdentity" = None,
        value: typing.Any = None,
        multivariate_feature_state_values: typing.List[
            DjangoMultivariateFeatureStateValue
        ] = None,
    ):
        self.id = id
        self.feature_segment = feature_segment
        self.identity = identity
        self.feature = feature
        self.enabled = enabled
        self.value = value
        self.multivariate_feature_state_values = (
            DjangoMultivariateFeatureStateValueRelatedManager(
                multivariate_feature_state_values or []
            )
        )

    def get_feature_state_value(self):
        return self.value


@dataclass
class DjangoFeatureStateRelatedManager:
    feature_states: typing.List[DjangoFeatureState]

    def filter(self, **filter_kwargs) -> typing.List[DjangoFeatureState]:
        return self.feature_states

    def all(self) -> typing.List[DjangoFeatureState]:
        return self.feature_states


class DjangoEnvironment:
    def __init__(
        self,
        id: int,
        project: DjangoProject,
        name: str = "Test Environment",
        api_key: str = "api-key",
        feature_states: typing.List[DjangoFeatureState] = None,
    ):
        if feature_states:
            assert not any(
                fs.feature_segment or fs.identity for fs in feature_states
            ), "FeatureStates for an environment must not have identity or segment"

        self.id = id
        self.name = name
        self.api_key = api_key
        self.project = project
        self.feature_states = DjangoFeatureStateRelatedManager(feature_states or [])


@dataclass
class DjangoTrait:
    trait_key: str
    trait_value: typing.Any


@dataclass
class DjangoTraitRelatedManager:
    traits: typing.List[DjangoTrait]

    def filter(self, **filter_kwargs) -> typing.List[DjangoTrait]:
        return self.traits


class DjangoIdentity:
    def __init__(
        self,
        id: int,
        identifier: str,
        created_date: datetime,
        environment: DjangoEnvironment,
        feature_states: typing.List[DjangoFeatureState] = None,
        identity_traits: typing.List[DjangoTrait] = None,
    ):
        if feature_states:
            assert not any(
                fs.feature_segment for fs in feature_states
            ), "FeatureStates for an identity cannot have a segment"

        self.id = id
        self.identifier = identifier
        self.created_date = created_date
        self.environment = environment
        self.identity_features = DjangoFeatureStateRelatedManager(feature_states or [])
        self.identity_traits = DjangoTraitRelatedManager(identity_traits or [])
