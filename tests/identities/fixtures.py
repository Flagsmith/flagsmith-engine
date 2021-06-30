from flag_engine.segments import constants
from flag_engine.segments.models import Segment, SegmentCondition, SegmentRule

trait_key_1 = "email"
trait_value_1 = "user@example.com"

trait_key_2 = "num_purchase"
trait_value_2 = 12

trait_key_3 = "date_joined"
trait_value_3 = "2021-01-01"


empty_segment = Segment(id=1, name="empty_segment")
segment_single_condition = Segment(
    id=2,
    name="segment_one_condition",
    rules=[
        SegmentRule(
            type=constants.ALL_RULE,
            conditions=[
                SegmentCondition(
                    operator=constants.EQUAL,
                    property_=trait_key_1,
                    value=trait_value_1,
                )
            ],
        )
    ],
)
segment_multiple_conditions_all = Segment(
    id=3,
    name="segment_multiple_conditions_all",
    rules=[
        SegmentRule(
            type=constants.ALL_RULE,
            conditions=[
                SegmentCondition(
                    operator=constants.EQUAL,
                    property_=trait_key_1,
                    value=trait_value_1,
                ),
                SegmentCondition(
                    operator=constants.EQUAL,
                    property_=trait_key_2,
                    value=trait_value_2,
                ),
            ],
        )
    ],
)
segment_multiple_conditions_any = Segment(
    id=4,
    name="segment_multiple_conditions_all",
    rules=[
        SegmentRule(
            type=constants.ANY_RULE,
            conditions=[
                SegmentCondition(
                    operator=constants.EQUAL,
                    property_=trait_key_1,
                    value=trait_value_1,
                ),
                SegmentCondition(
                    operator=constants.EQUAL,
                    property_=trait_key_2,
                    value=trait_value_2,
                ),
            ],
        )
    ],
)
segment_nested_rules_all = Segment(
    id=5,
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
                            property_=trait_key_1,
                            value=trait_value_1,
                        ),
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property_=trait_key_2,
                            value=trait_value_2,
                        ),
                    ],
                ),
                SegmentRule(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property_=trait_key_3,
                            value=trait_value_3,
                        )
                    ],
                ),
            ],
        )
    ],
)
segment_nested_rules_any = Segment(
    id=6,
    name="segment_nested_rules_all",
    rules=[
        SegmentRule(
            type=constants.ANY_RULE,
            rules=[
                SegmentRule(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property_=trait_key_1,
                            value=trait_value_1,
                        ),
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property_=trait_key_2,
                            value=trait_value_2,
                        ),
                    ],
                ),
                SegmentRule(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentCondition(
                            operator=constants.EQUAL,
                            property_=trait_key_3,
                            value=trait_value_3,
                        )
                    ],
                ),
            ],
        )
    ],
)
