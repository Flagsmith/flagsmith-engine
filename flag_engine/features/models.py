import math
import typing
import uuid

from annotated_types import Ge, Le, SupportsLt
from pydantic import UUID4, BaseModel, Field, model_validator
from pydantic_collections import BaseCollectionModel
from typing_extensions import Annotated

from flag_engine.utils.exceptions import InvalidPercentageAllocation
from flag_engine.utils.hashing import get_hashed_percentage_for_object_ids


class FeatureModel(BaseModel):
    id: int
    name: str
    type: str

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FeatureModel) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class MultivariateFeatureOptionModel(BaseModel):
    value: typing.Any
    id: typing.Optional[int] = None


class MultivariateFeatureStateValueModel(BaseModel):
    multivariate_feature_option: MultivariateFeatureOptionModel
    percentage_allocation: Annotated[float, Ge(0), Le(100)]
    id: typing.Optional[int] = None
    mv_fs_value_uuid: UUID4 = Field(default_factory=uuid.uuid4)


class FeatureSegmentModel(BaseModel):
    priority: typing.Optional[int] = None


class MultivariateFeatureStateValueList(
    BaseCollectionModel[MultivariateFeatureStateValueModel]  # type: ignore[misc,no-any-unimported]
):
    @staticmethod
    def _ensure_correct_percentage_allocations(
        value: typing.List[MultivariateFeatureStateValueModel],
    ) -> typing.List[MultivariateFeatureStateValueModel]:
        if (
            sum(
                multivariate_feature_state.percentage_allocation
                for multivariate_feature_state in value
            )
            > 100
        ):
            raise InvalidPercentageAllocation(
                "Total percentage allocation for feature must be less or equal to 100 percent"
            )
        return value

    percentage_allocations_model_validator = model_validator(mode="after")(
        _ensure_correct_percentage_allocations
    )

    def append(
        self,
        multivariate_feature_state_value: MultivariateFeatureStateValueModel,
    ) -> None:
        self._ensure_correct_percentage_allocations(
            [*self, multivariate_feature_state_value],
        )
        super().append(multivariate_feature_state_value)


class FeatureStateModel(BaseModel, validate_assignment=True):
    feature: FeatureModel
    enabled: bool
    django_id: typing.Optional[int] = None
    feature_segment: typing.Optional[FeatureSegmentModel] = None
    featurestate_uuid: UUID4 = Field(default_factory=uuid.uuid4)
    feature_state_value: typing.Any = None
    multivariate_feature_state_values: MultivariateFeatureStateValueList = Field(
        default_factory=MultivariateFeatureStateValueList
    )

    def set_value(self, value: typing.Any) -> None:
        self.feature_state_value = value

    def get_value(self, identity_id: typing.Union[None, int, str] = None) -> typing.Any:
        """
        Get the value of the feature state.

        :param identity_id: a unique identifier for the identity, can be either a
            numeric id or a string but must be unique for the identity.
        :return: the value of the feature state.
        """
        if identity_id and len(self.multivariate_feature_state_values) > 0:
            return self._get_multivariate_value(identity_id)
        return self.feature_state_value

    def is_higher_segment_priority(self, other: "FeatureStateModel") -> bool:
        """
        Returns `True` if `self` is higher segment priority than `other`
        (i.e. has lower value for feature_segment.priority)

        NOTE:
            A segment will be considered higher priority only if:
            1. `other` does not have a feature segment(i.e: it is an environment feature state or it's a
            feature state with feature segment but from an old document that does not have `feature_segment.priority`)
            but `self` does.

            2. `other` have a feature segment with high priority

        """

        if other_feature_segment := other.feature_segment:
            if (
                other_feature_segment_priority := other_feature_segment.priority
            ) is not None:
                return (
                    getattr(
                        self.feature_segment,
                        "priority",
                        math.inf,
                    )
                    < other_feature_segment_priority
                )
        return False

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
        start_percentage = 0.0

        def _mv_fs_sort_key(mv_value: MultivariateFeatureStateValueModel) -> SupportsLt:
            return mv_value.id or mv_value.mv_fs_value_uuid

        for mv_value in sorted(
            self.multivariate_feature_state_values,
            key=_mv_fs_sort_key,
        ):
            limit = mv_value.percentage_allocation + start_percentage
            if start_percentage <= percentage_value < limit:
                return mv_value.multivariate_feature_option.value

            start_percentage = limit

        # default to return the control value if no MV values found, although this
        # should never happen
        return self.feature_state_value
