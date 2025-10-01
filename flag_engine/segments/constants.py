from flag_engine.segments.types import ConditionOperator, RuleType

# Segment Rules
ALL_RULE: RuleType = "ALL"
ANY_RULE: RuleType = "ANY"
NONE_RULE: RuleType = "NONE"

# Segment Condition Operators
EQUAL: ConditionOperator = "EQUAL"
GREATER_THAN: ConditionOperator = "GREATER_THAN"
LESS_THAN: ConditionOperator = "LESS_THAN"
LESS_THAN_INCLUSIVE: ConditionOperator = "LESS_THAN_INCLUSIVE"
CONTAINS: ConditionOperator = "CONTAINS"
GREATER_THAN_INCLUSIVE: ConditionOperator = "GREATER_THAN_INCLUSIVE"
NOT_CONTAINS: ConditionOperator = "NOT_CONTAINS"
NOT_EQUAL: ConditionOperator = "NOT_EQUAL"
REGEX: ConditionOperator = "REGEX"
PERCENTAGE_SPLIT: ConditionOperator = "PERCENTAGE_SPLIT"
MODULO: ConditionOperator = "MODULO"
IS_SET: ConditionOperator = "IS_SET"
IS_NOT_SET: ConditionOperator = "IS_NOT_SET"
IN: ConditionOperator = "IN"

# Weakest possible priority for segment overrides
DEFAULT_PRIORITY = float("inf")
