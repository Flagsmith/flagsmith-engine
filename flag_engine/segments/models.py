import re
import typing
from contextlib import suppress

import semver
from pydantic import BaseModel, Field

from flag_engine.features.models import FeatureStateModel
from flag_engine.segments import constants
from flag_engine.segments.types import ConditionOperator, RuleType
from flag_engine.utils.semver import is_semver
from flag_engine.utils.types import get_casting_function


class SegmentConditionModel(BaseModel):
    _EXCEPTION_OPERATOR_METHODS = {
        constants.NOT_CONTAINS: "evaluate_not_contains",
        constants.REGEX: "evaluate_regex",
        constants.MODULO: "evaluate_modulo",
        constants.IN: "evaluate_in",
    }

    operator: ConditionOperator
    value: typing.Optional[str] = None
    property_: typing.Optional[str] = None

    def matches_trait_value(self, trait_value: typing.Any) -> bool:
        # TODO: move this logic to the evaluator module
        with suppress(ValueError):
            if type(self.value) is str and is_semver(self.value):
                trait_value = semver.VersionInfo.parse(trait_value)
            if self.operator in self._EXCEPTION_OPERATOR_METHODS:
                evaluator_function = getattr(
                    self, self._EXCEPTION_OPERATOR_METHODS.get(self.operator)
                )
                return evaluator_function(trait_value)

            matching_function_name = {
                constants.EQUAL: "__eq__",
                constants.GREATER_THAN: "__gt__",
                constants.GREATER_THAN_INCLUSIVE: "__ge__",
                constants.LESS_THAN: "__lt__",
                constants.LESS_THAN_INCLUSIVE: "__le__",
                constants.NOT_EQUAL: "__ne__",
                constants.CONTAINS: "__contains__",
            }.get(self.operator)
            matching_function = getattr(
                trait_value, matching_function_name, lambda v: False
            )
            to_same_type_as_trait_value = get_casting_function(trait_value)
            return matching_function(to_same_type_as_trait_value(self.value))

        return False

    def evaluate_not_contains(self, trait_value: typing.Iterable) -> bool:
        return self.value not in trait_value

    def evaluate_regex(self, trait_value: str) -> bool:
        return (
            trait_value is not None
            and re.compile(str(self.value)).match(str(trait_value)) is not None
        )

    def evaluate_modulo(self, trait_value: typing.Union[str, int, float, bool]) -> bool:
        if type(trait_value) not in (int, float):
            return False
        try:
            divisor, remainder = self.value.split("|")
            divisor = float(divisor)
            remainder = float(remainder)
        except ValueError:
            return False
        return trait_value % divisor == remainder

    def evaluate_in(self, trait_value) -> bool:
        try:
            return str(trait_value) in self.value.split(",")
        except AttributeError:
            return False


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
