import typing
from dataclasses import dataclass, field
from datetime import datetime

from flag_engine.utils.datetime import utcnow_with_tz


@dataclass
class DjangoSegmentCondition:
    operator: str
    value: str
    property: str = None  # property can be none e.g. for % split operator


@dataclass
class DjangoSegmentConditionRelatedObjectManager:
    conditions: typing.List[DjangoSegmentCondition]

    def all(self) -> typing.List[DjangoSegmentCondition]:
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

    def all(self) -> typing.List[DjangoSegment]:
        return self.segments


class DjangoFeatureSegment:
    def __init__(
        self,
        id_: int,
        environment: "DjangoEnvironment",
        feature_states: typing.List["DjangoFeatureState"] = None,
    ):
        self.id = id_
        self.environment = environment
        self.feature_states = DjangoFeatureStateRelatedManager(feature_states or [])


@dataclass
class DjangoFeatureSegmentRelatedObjectManager:
    feature_segments: typing.List[DjangoFeatureSegment]

    def all(self) -> typing.List[DjangoFeatureSegment]:
        return self.feature_segments


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

    def add_segment(self, segment: DjangoSegment):
        self.segments.segments.append(segment)


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

    def all(self) -> typing.List[DjangoMultivariateFeatureStateValue]:
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
        version: int = 1,
        live_from: datetime = None,
    ):
        self.id = id
        self.feature_segment_id = getattr(feature_segment, "id", None)
        self.feature_segment = feature_segment
        self.identity_id = getattr(identity, "id", None)
        self.identity = identity
        self.feature = feature
        self.enabled = enabled
        self.value = value
        self.multivariate_feature_state_values = (
            DjangoMultivariateFeatureStateValueRelatedManager(
                multivariate_feature_state_values or []
            )
        )
        self.version = version
        self.live_from = live_from or utcnow_with_tz()

    def get_feature_state_value(self):
        return self.value

    @property
    def feature_id(self):
        return self.feature.id


@dataclass
class DjangoFeatureStateRelatedManager:
    feature_states: typing.List[DjangoFeatureState]

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
class DjangoEnvironmentAPIKey:
    id: int
    environment: DjangoEnvironment
    key: str
    created_at: datetime
    name: str
    expires_at: datetime = None
    active: bool = True


@dataclass
class DjangoTrait:
    trait_key: str
    trait_value: typing.Any


@dataclass
class DjangoTraitRelatedManager:
    traits: typing.List[DjangoTrait]

    def all(self) -> typing.List[DjangoTrait]:
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
