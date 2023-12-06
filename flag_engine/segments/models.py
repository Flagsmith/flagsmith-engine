import typing

from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Annotated

from flag_engine.features.models import FeatureStateModel
from flag_engine.segments import constants
from flag_engine.segments.types import ConditionOperator, RuleType, SegmentType

LaxStr = Annotated[str, BeforeValidator(lambda x: str(x))]


class SegmentConditionModel(BaseModel):
    operator: ConditionOperator
    value: typing.Optional[LaxStr] = None
    property_: typing.Optional[str] = None


class SegmentRuleModel(BaseModel):
    type: RuleType
    rules: typing.List["SegmentRuleModel"] = Field(default_factory=list)
    conditions: typing.List[SegmentConditionModel] = Field(default_factory=list)

    @staticmethod
    def none(iterable: typing.Iterable[object]) -> bool:
        return not any(iterable)

    @property
    def matching_function(self) -> typing.Callable[[typing.Iterable[object]], bool]:
        return {
            constants.ANY_RULE: any,
            constants.ALL_RULE: all,
            constants.NONE_RULE: SegmentRuleModel.none,
        }[self.type]


class SegmentMetadata(BaseModel):
    type: SegmentType = "SEGMENT"
    identity_identifier: typing.Optional[str] = None
    identity_uuid: typing.Optional[str] = None


class SegmentModel(BaseModel):
    id: int
    name: str
    rules: typing.List[SegmentRuleModel] = Field(default_factory=list)
    feature_states: typing.List[FeatureStateModel] = Field(default_factory=list)
    meta: typing.Optional[SegmentMetadata] = None
