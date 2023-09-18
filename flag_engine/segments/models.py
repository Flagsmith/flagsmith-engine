import typing

from pydantic import BaseModel, Field

from flag_engine.features.models import FeatureStateModel
from flag_engine.segments import constants
from flag_engine.segments.types import ConditionOperator, RuleType


class SegmentConditionModel(BaseModel):
    operator: ConditionOperator
    value: typing.Optional[str] = None
    property_: typing.Optional[str] = None


class SegmentRuleModel(BaseModel):
    type: RuleType
    rules: typing.List["SegmentRuleModel"] = Field(default_factory=list)
    conditions: typing.List[SegmentConditionModel] = Field(default_factory=list)

    @staticmethod
    def none(iterable: typing.Iterable) -> bool:
        return not any(iterable)

    @property
    def matching_function(self) -> callable:
        return {
            constants.ANY_RULE: any,
            constants.ALL_RULE: all,
            constants.NONE_RULE: SegmentRuleModel.none,
        }.get(self.type)


class SegmentModel(BaseModel):
    id: int
    name: str
    rules: typing.List[SegmentRuleModel] = Field(default_factory=list)
    feature_states: typing.List[FeatureStateModel] = Field(default_factory=list)
