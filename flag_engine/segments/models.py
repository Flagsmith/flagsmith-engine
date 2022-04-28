import re
import typing
from dataclasses import dataclass, field

import semver

from flag_engine.features.models import FeatureStateModel
from flag_engine.segments import constants
from flag_engine.utils.models import FlagsmithValue, FlagsmithValueType
from flag_engine.utils.semver import is_semver, remove_semver_suffix


@dataclass
class SegmentConditionModel:
    operator: str
    value: str
    property_: str = None

    def matches_trait_value(self, trait_value: FlagsmithValue) -> bool:
        # TODO: move this logic to the evaluator module
        if trait_value.value_type == FlagsmithValueType.STRING and is_semver(
            self.value
        ):
            return self.evaluate_semver_match(trait_value.value, str(self.value))
        elif trait_value.value_type == FlagsmithValueType.BOOLEAN:
            return self.evaluate_bool_match(
                trait_value.value in ("True", "true", "1"),
                str(self.value) in ("True", "true", "1"),
            )
        elif trait_value.value_type == FlagsmithValueType.INTEGER:
            return self.evaluate_number_match(int(trait_value.value), int(self.value))
        elif trait_value.value_type == FlagsmithValueType.FLOAT:
            return self.evaluate_number_match(
                float(trait_value.value), float(self.value)
            )
        elif trait_value.value_type == FlagsmithValueType.STRING:
            return self.evaluate_string_match(trait_value.value, str(self.value))

        return False

    def evaluate_string_match(
        self, value_from_trait: str, value_from_segment: str
    ) -> bool:
        if self.operator == constants.EQUAL:
            return value_from_trait == value_from_segment
        elif self.operator == constants.NOT_EQUAL:
            return value_from_trait != value_from_segment
        elif self.operator == constants.CONTAINS:
            return value_from_segment in value_from_trait
        elif self.operator == constants.NOT_CONTAINS:
            return value_from_segment not in value_from_trait
        elif self.operator == constants.REGEX:
            return re.compile(value_from_segment).match(value_from_trait) is not None
        return False

    def evaluate_bool_match(
        self, value_from_trait: bool, value_from_segment: bool
    ) -> bool:
        if self.operator == constants.EQUAL:
            return value_from_trait == value_from_segment
        elif self.operator == constants.NOT_EQUAL:
            return value_from_trait != value_from_segment
        return False

    def evaluate_number_match(
        self,
        value_from_trait: typing.Union[int, float, semver.VersionInfo],
        value_from_segment: typing.Union[int, float, semver.VersionInfo],
    ):
        if self.operator == constants.EQUAL:
            return value_from_trait == value_from_segment
        elif self.operator == constants.NOT_EQUAL:
            return value_from_trait != value_from_segment
        elif self.operator == constants.LESS_THAN:
            return value_from_trait < value_from_segment
        elif self.operator == constants.LESS_THAN_INCLUSIVE:
            return value_from_trait <= value_from_segment
        elif self.operator == constants.GREATER_THAN:
            return value_from_trait > value_from_segment
        elif self.operator == constants.GREATER_THAN_INCLUSIVE:
            return value_from_trait >= value_from_segment
        return False

    def evaluate_semver_match(
        self, value_from_trait: str, value_from_segment: str
    ) -> bool:
        value_from_segment = semver.VersionInfo.parse(
            remove_semver_suffix(value_from_segment)
        )
        value_from_trait = semver.VersionInfo.parse(value_from_trait)
        return self.evaluate_number_match(value_from_trait, value_from_segment)


@dataclass
class SegmentRuleModel:
    type: str
    rules: typing.List["SegmentRuleModel"] = field(default_factory=list)
    conditions: typing.List[SegmentConditionModel] = field(default_factory=list)

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


@dataclass
class SegmentModel:
    id: int
    name: str
    rules: typing.List[SegmentRuleModel] = field(default_factory=list)
    feature_states: typing.List[FeatureStateModel] = field(default_factory=list)
