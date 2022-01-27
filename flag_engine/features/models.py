import typing
import uuid
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
    id: int = None


@dataclass
class MultivariateFeatureStateValueModel:
    multivariate_feature_option: MultivariateFeatureOptionModel
    percentage_allocation: float
    id: int = None
    mv_fs_value_uuid: str = field(default_factory=uuid.uuid4)


@dataclass
class FeatureStateModel:
    feature: FeatureModel
    enabled: bool
    django_id: int = None
    featurestate_uuid: str = field(default_factory=uuid.uuid4)
    _value: typing.Any = field(default=None, init=False)
    multivariate_feature_state_values: typing.List[
        MultivariateFeatureStateValueModel
    ] = field(default_factory=list)

    def set_value(self, value: typing.Any):
        self._value = value

    def get_value(self, identity_id: typing.Union[int, str] = None) -> typing.Any:
        """
        Get the value of the feature state.

        :param identity_id: a unique identifier for the identity, can be either a
            numeric id or a string but must be unique for the identity.
        :return: the value of the feature state.
        """
        if identity_id and len(self.multivariate_feature_state_values) > 0:
            return self._get_multivariate_value(identity_id)
        return self._value

    def get_feature_state_value(self):
        """Mimick django method name to simplify serialization logic"""
        return self.get_value()

    def _get_multivariate_value(
        self, identity_id: typing.Union[int, str]
    ) -> typing.Any:
        percentage_value = get_hashed_percentage_for_object_ids(
            [self.django_id or self.featurestate_uuid, identity_id]
        )

        # Iterate over the mv options in order of id (so we get the same value each
        # time) to determine the correct value to return to the identity based on
        # the percentage allocations of the multivariate options. This gives us a
        # way to ensure that the same value is returned every time we use the same
        # percentage value.
        start_percentage = 0
        for mv_value in sorted(
            self.multivariate_feature_state_values,
            key=lambda v: v.id or v.mv_fs_value_uuid,
        ):
            limit = mv_value.percentage_allocation + start_percentage
            if start_percentage <= percentage_value < limit:
                return mv_value.multivariate_feature_option.value

            start_percentage = limit

        # default to return the control value if no MV values found, although this
        # should never happen
        return self._value
