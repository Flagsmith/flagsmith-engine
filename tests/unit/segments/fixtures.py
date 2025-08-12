from flag_engine.context.types import SegmentCondition, SegmentContext, SegmentRule
from flag_engine.segments import constants

trait_key_1 = "email"
trait_value_1 = "user@example.com"

trait_key_2 = "num_purchase"
trait_value_2 = "12"

trait_key_3 = "date_joined"
trait_value_3 = "2021-01-01"

empty_segment = SegmentContext(key=str(1), name="empty_segment", rules=[])

segment_single_condition = SegmentContext(
    key=str(2),
    name="segment_one_condition",
    rules=[
        SegmentRule(
            type=constants.ALL_RULE,
            conditions=[
                SegmentCondition(
                    operator=constants.EQUAL,
                    property=trait_key_1,
                    value=trait_value_1,
                )
            ],
        )
    ],
)

segment_multiple_conditions_all = SegmentContext(
    key=str(3),
    name="segment_multiple_conditions_all",
    rules=[
        SegmentRule(
            type=constants.ALL_RULE,
            conditions=[
                SegmentCondition(
                    operator=constants.EQUAL,
                    property=trait_key_1,
                    value=trait_value_1,
                ),
                SegmentCondition(
                    operator=constants.EQUAL,
                    property=trait_key_2,
                    value=trait_value_2,
                ),
            ],
        )
    ],
)

segment_multiple_conditions_any = SegmentContext(
    key=str(4),
    name="segment_multiple_conditions_all",
    rules=[
        SegmentRule(
            type=constants.ANY_RULE,
            conditions=[
                SegmentCondition(
                    operator=constants.EQUAL,
                    property=trait_key_1,
                    value=trait_value_1,
                ),
                SegmentCondition(
                    operator=constants.EQUAL,
                    property=trait_key_2,
                    value=trait_value_2,
                ),
            ],
        )
    ],
)

segment_nested_rules = SegmentContext(
    key=str(5),
    name="segment_nested_rules_all",
    rules=[
        SegmentRule(
            type=constants.ALL_RULE,
            rules=[
                SegmentRule(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property=trait_key_1,
                            value=trait_value_1,
                        ),
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property=trait_key_2,
                            value=trait_value_2,
                        ),
                    ],
                ),
                SegmentRule(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property=trait_key_3,
                            value=trait_value_3,
                        )
                    ],
                ),
            ],
        )
    ],
)

segment_conditions_and_nested_rules = SegmentContext(
    key=str(6),
    name="segment_multiple_conditions_all_and_nested_rules",
    rules=[
        SegmentRule(
            type=constants.ALL_RULE,
            conditions=[
                SegmentCondition(
                    operator=constants.EQUAL,
                    property=trait_key_1,
                    value=trait_value_1,
                )
            ],
            rules=[
                SegmentRule(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property=trait_key_2,
                            value=trait_value_2,
                        ),
                    ],
                ),
                SegmentRule(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property=trait_key_3,
                            value=trait_value_3,
                        )
                    ],
                ),
            ],
        )
    ],
)
