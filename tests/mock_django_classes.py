import typing
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DjangoOrganisation:
    id: int
    name: str
    stop_serving_flags: bool = False
    persist_trait_data: bool = True
    feature_analytics: bool = True


@dataclass
class DjangoProject:
    id: int
    name: str
    organisation: DjangoOrganisation
    hide_disabled_flags: bool = False


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


@dataclass
class DjangoSegment:
    id: int


@dataclass
class DjangoFeatureSegment:
    id: int
    segment: DjangoSegment


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
