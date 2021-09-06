import typing
from dataclasses import dataclass, field

from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids


@dataclass
class FeatureModel:
    id: int
    name: str
    type: str

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


@dataclass
class MultivariateFeatureOptionModel:
    value: typing.Any


@dataclass
class MultivariateFeatureStateValueModel:
    id: int
    multivariate_feature_option: MultivariateFeatureOptionModel
    percentage_allocation: float


@dataclass
class FeatureStateModel:
    id: int
    feature: FeatureModel
    enabled: bool
    _value: typing.Any = field(default=None, init=False)
    multivariate_feature_state_values: typing.List[
        MultivariateFeatureStateValueModel
    ] = field(default_factory=list)

    def set_value(self, value: typing.Any):
        self._value = value

    def get_value(self, identity_id: int = None):
        if identity_id and len(self.multivariate_feature_state_values) > 0:
            return self._get_multivariate_value(identity_id)
        return self._value

    def get_feature_state_value(self):
        """Mimick django method name to simplify serialization logic"""
        return self.get_value()

    def _get_multivariate_value(self, identity_id: int) -> typing.Any:
        percentage_value = get_hashed_percentage_for_object_ids([self.id, identity_id])

        # Iterate over the mv options in order of id (so we get the same value each
        # time) to determine the correct value to return to the identity based on
        # the percentage allocations of the multivariate options. This gives us a
        # way to ensure that the same value is returned every time we use the same
        # percentage value.
        start_percentage = 0
        for mv_value in sorted(
            self.multivariate_feature_state_values, key=lambda v: v.id
        ):
            limit = mv_value.percentage_allocation + start_percentage
            if start_percentage <= percentage_value < limit:
                return mv_value.multivariate_feature_option.value

            start_percentage = limit

        # default to return the control value if no MV values found, although this
        # should never happen
        return self._value
