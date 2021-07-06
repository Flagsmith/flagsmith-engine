import typing
from dataclasses import dataclass, field


@dataclass
class DjangoProject:
    id: int
    name: str


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
    multivariate_feature_state_values: typing.List = field(default_factory=list)

    def all(self):
        return self.multivariate_feature_state_values


class DjangoFeatureState:
    def __init__(
        self,
        id: int,
        feature: DjangoFeature,
        enabled: bool,
        value: typing.Any = None,
        multivariate_feature_state_values: typing.List[
            DjangoMultivariateFeatureStateValue
        ] = None,
    ):
        self.id = id
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

    def all(self):
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

    def all(self):
        return self.traits


class DjangoIdentity:
    def __init__(
        self,
        id: int,
        identifier: str,
        environment: DjangoEnvironment,
        feature_states: typing.List[DjangoFeatureState] = None,
        identity_traits: typing.List[DjangoTrait] = None,
    ):
        self.id = id
        self.identifier = identifier
        self.environment = environment
        self.identity_features = DjangoFeatureStateRelatedManager(feature_states or [])
        self.identity_traits = DjangoTraitRelatedManager(identity_traits or [])
