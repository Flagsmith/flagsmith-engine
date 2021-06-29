from flag_engine.segments import constants
from flag_engine.segments.schemas import SegmentRuleSchema


def test_segment_rule_validation_passes_if_rules_given_only():
    # Given
    data = {
        "type": constants.ALL_RULE,
        "rules": [
            {
                "type": constants.ANY_RULE,
                "conditions": [
                    {"operator": constants.EQUAL, "property": "foo", "value": "bar"}
                ],
            }
        ],
    }
    segment_rule_schema = SegmentRuleSchema()

    # When
    errors = segment_rule_schema.validate(data)

    # Then
    assert not errors


def test_segment_rule_validation_passes_if_conditions_given_only():
    # Given
    data = {
        "type": constants.ALL_RULE,
        "conditions": [
            {"operator": constants.EQUAL, "property": "foo", "value": "bar"}
        ],
    }
    segment_rule_schema = SegmentRuleSchema()

    # When
    errors = segment_rule_schema.validate(data)

    # Then
    assert not errors


def test_segment_rule_validation_fails_if_rules_and_conditions_given():
    # Given
    data = {
        "type": constants.ALL_RULE,
        "rules": [{"type": constants.ANY_RULE}],
        "conditions": [
            {"operator": constants.EQUAL, "property": "foo", "value": "bar"}
        ],
    }
    segment_rule_schema = SegmentRuleSchema()

    # When
    errors = segment_rule_schema.validate(data)

    # Then
    assert (
        errors["_schema"][0] == "Segment rule must not have both rules and conditions"
    )
