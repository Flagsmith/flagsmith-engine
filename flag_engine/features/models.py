import typing
import uuid
import warnings

from annotated_types import Ge, Le
from pydantic import UUID4, BaseModel, Field, model_validator
from pydantic_collections import BaseCollectionModel
from typing_extensions import Annotated

from flag_engine.utils.exceptions import InvalidPercentageAllocation


class FeatureModel(BaseModel):
    id: int
    name: str
    type: str

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FeatureModel) and self.id == other.id


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
        DEPRECATED: Get the value of the feature state.
        Use the `feature_state_value` field directly instead.

        :param identity_id: a unique identifier for the identity, can be either a
            numeric id or a string but must be unique for the identity.
        :return: the value of the feature state.
        """
        warnings.warn(
            "get_value is deprecated, use feature_state_value directly.",
            DeprecationWarning,
        )
        return self.feature_state_value
