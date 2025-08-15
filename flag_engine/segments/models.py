import typing

from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Annotated

from flag_engine.features.models import FeatureStateModel
from flag_engine.segments.types import ConditionOperator, RuleType
from flag_engine.segments.utils import get_matching_function

LaxStr = Annotated[str, BeforeValidator(lambda x: str(x))]


class SegmentConditionModel(BaseModel):
    operator: ConditionOperator
    value: typing.Optional[LaxStr] = None
    property_: typing.Optional[str] = None


class SegmentRuleModel(BaseModel):
    type: RuleType
    rules: typing.List["SegmentRuleModel"] = Field(default_factory=list)
    conditions: typing.List[SegmentConditionModel] = Field(default_factory=list)

    @property
    def matching_function(self) -> typing.Callable[[typing.Iterable[object]], bool]:
        return get_matching_function(self.type)


class SegmentModel(BaseModel):
    id: int
    name: str
    rules: typing.List[SegmentRuleModel] = Field(default_factory=list)
    feature_states: typing.List[FeatureStateModel] = Field(default_factory=list)
