import typing
from dataclasses import dataclass, field

from flag_engine.segments import constants
from flag_engine.features.models import FeatureState


@dataclass
class SegmentCondition:
    operator: str
    value: typing.Any
    property_: str = None

    def matches_trait_value(self, trait_value: typing.Any) -> bool:
        matching_function_name = {
            constants.EQUAL: "__eq__",
            constants.GREATER_THAN: "__gt__",
            constants.GREATER_THAN_INCLUSIVE: "__ge__",
            constants.LESS_THAN: "__lt__",
            constants.LESS_THAN_INCLUSIVE: "__le__",
            constants.NOT_EQUAL: "__ne__",
            constants.CONTAINS: "__contains__",
            constants.NOT_CONTAINS: "__contains__",
        }.get(self.operator)

        matching_function = getattr(
            trait_value, matching_function_name, lambda v: False
        )
        result = matching_function(self.value)

        if self.operator == constants.NOT_CONTAINS:
            # negate the contains result as there is no built in method for notcontains
            return not result

        return result


@dataclass
class SegmentRule:
    type: str
    rules: typing.List["SegmentRule"] = field(default_factory=list)
    conditions: typing.List[SegmentCondition] = field(default_factory=list)

    @staticmethod
    def none(iterable: typing.Iterable) -> bool:
        return not any(iterable)

    @property
    def matching_function(self) -> callable:
        return {
            constants.ANY_RULE: any,
            constants.ALL_RULE: all,
            constants.NONE_RULE: SegmentRule.none,
        }.get(self.type)


@dataclass
class Segment:
    id: int
    name: str
    rules: typing.List[SegmentRule]


@dataclass
class SegmentOverride:
    segment: Segment
    feature_state: FeatureState
