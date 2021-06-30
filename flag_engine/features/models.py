import typing
from dataclasses import dataclass, field


@dataclass
class Feature:
    id: int
    name: str

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


@dataclass
class MultivariateFeatureOption:
    value: typing.Any


class MultivariateFeatureStateValue:
    multivariate_feature_option: MultivariateFeatureOption
    percentage_allocation: float


@dataclass
class FeatureState:
    feature: Feature
    enabled: bool
    value: typing.Any = None
    multivariate_values: typing.List[MultivariateFeatureStateValue] = field(
        default_factory=list
    )
