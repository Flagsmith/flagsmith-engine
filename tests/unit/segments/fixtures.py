from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)

trait_key_1 = "email"
trait_value_1 = "user@example.com"

trait_key_2 = "num_purchase"
trait_value_2 = "12"

trait_key_3 = "date_joined"
trait_value_3 = "2021-01-01"

identifier = "identity_1"

empty_segment = SegmentModel(id=1, name="empty_segment")
segment_single_condition = SegmentModel(
    id=2,
    name="segment_one_condition",
    rules=[
        SegmentRuleModel(
            type=constants.ALL_RULE,
            conditions=[
                SegmentConditionModel(
                    operator=constants.EQUAL,
                    property_=trait_key_1,
                    value=trait_value_1,
                )
            ],
        )
    ],
)
segment_multiple_conditions_all = SegmentModel(
    id=3,
    name="segment_multiple_conditions_all",
    rules=[
        SegmentRuleModel(
            type=constants.ALL_RULE,
            conditions=[
                SegmentConditionModel(
                    operator=constants.EQUAL,
                    property_=trait_key_1,
                    value=trait_value_1,
                ),
                SegmentConditionModel(
                    operator=constants.EQUAL,
                    property_=trait_key_2,
                    value=trait_value_2,
                ),
            ],
        )
    ],
)
segment_multiple_conditions_any = SegmentModel(
    id=4,
    name="segment_multiple_conditions_all",
    rules=[
        SegmentRuleModel(
            type=constants.ANY_RULE,
            conditions=[
                SegmentConditionModel(
                    operator=constants.EQUAL,
                    property_=trait_key_1,
                    value=trait_value_1,
                ),
                SegmentConditionModel(
                    operator=constants.EQUAL,
                    property_=trait_key_2,
                    value=trait_value_2,
                ),
            ],
        )
    ],
)
segment_nested_rules = SegmentModel(
    id=5,
    name="segment_nested_rules_all",
    rules=[
        SegmentRuleModel(
            type=constants.ALL_RULE,
            rules=[
                SegmentRuleModel(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentConditionModel(
                            operator=constants.EQUAL,
                            property_=trait_key_1,
                            value=trait_value_1,
                        ),
                        SegmentConditionModel(
                            operator=constants.EQUAL,
                            property_=trait_key_2,
                            value=trait_value_2,
                        ),
                    ],
                ),
                SegmentRuleModel(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentConditionModel(
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
segment_conditions_and_nested_rules = SegmentModel(
    id=6,
    name="segment_multiple_conditions_all_and_nested_rules",
    rules=[
        SegmentRuleModel(
            type=constants.ALL_RULE,
            conditions=[
                SegmentConditionModel(
                    operator=constants.EQUAL,
                    property_=trait_key_1,
                    value=trait_value_1,
                )
            ],
            rules=[
                SegmentRuleModel(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentConditionModel(
                            operator=constants.EQUAL,
                            property_=trait_key_2,
                            value=trait_value_2,
                        ),
                    ],
                ),
                SegmentRuleModel(
                    type=constants.ALL_RULE,
                    conditions=[
                        SegmentConditionModel(
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
segment_identity_override = SegmentModel(
    id=7,
    name="dentity_override_identity_1_b6c2e2",
    rules=[
        SegmentRuleModel(
            type=constants.ALL_RULE,
            conditions=[
                SegmentConditionModel(
                    operator=constants.EQUAL,
                    property_=constants.SEGMENT_IDENTIFIER_PROPERTY_NAME,
                    value=identifier,
                )
            ],
        )
    ],
    meta={
        "identity_uuid": "d049c16b-e4dd-4830-b238-db2241c159e6",
        "identity_identifier": identifier,
        "type": "IDENTITY_OVERRIDE",
    },
)
