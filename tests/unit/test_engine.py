import json

from flag_engine.context.types import EvaluationContext, IdentityContext, SegmentContext
from flag_engine.engine import get_evaluation_result


def test_get_evaluation_result__no_overrides__returns_expected(
    context: EvaluationContext,
) -> None:
    # When
    result = get_evaluation_result(context)

    # Then
    assert result == {
        "context": context,
        "flags": [
            {
                "enabled": True,
                "feature_key": "1",
                "name": "feature_1",
                "reason": "DEFAULT",
                "value": None,
            },
            {
                "enabled": False,
                "feature_key": "2",
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        ],
        "segments": [],
    }


def test_get_evaluation_result__segment_override__returns_expected(
    context_in_segment: EvaluationContext,
) -> None:
    # When
    result = get_evaluation_result(context_in_segment)

    # Then
    assert result == {
        "context": context_in_segment,
        "flags": [
            {
                "enabled": False,
                "feature_key": "1",
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=my_segment",
                "value": "segment_override",
            },
            {
                "enabled": False,
                "feature_key": "2",
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        ],
        "segments": [{"key": "1", "name": "my_segment"}],
    }


def test_get_evaluation_result__identity_override__returns_expected(
    identity: IdentityContext,
    context: EvaluationContext,
) -> None:
    # Given
    identity_overrides_segment = SegmentContext(
        key="",
        name="identity_overrides",
        rules=[
            {
                "type": "ALL",
                "conditions": [
                    {
                        "property": "$.identity.identifier",
                        "operator": "IN",
                        "value": json.dumps([identity["identifier"]]),
                    },
                ],
            }
        ],
        overrides=[
            {
                "key": "5",
                "feature_key": "1",
                "name": "feature_1",
                "enabled": True,
                "value": "overridden_for_identity",
            }
        ],
    )
    context["segments"] = {"123": identity_overrides_segment}

    # When
    result = get_evaluation_result(context)

    # Then
    assert result == {
        "context": context,
        "flags": [
            {
                "enabled": True,
                "feature_key": "1",
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=identity_overrides",
                "value": "overridden_for_identity",
            },
            {
                "enabled": False,
                "feature_key": "2",
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        ],
        "segments": [
            {
                "key": "",
                "name": "identity_overrides",
            },
        ],
    }


def test_get_evaluation_result__two_segments_override_same_feature__returns_expected() -> (
    None
):
    # Given
    context_in_segments: EvaluationContext = {
        "environment": {"key": "api-key", "name": ""},
        "identity": {
            "identifier": "identity_2",
            "key": "api-key_identity_2",
            "traits": {"foo": "bar"},
        },
        "features": {
            "feature_1": {
                "key": "1",
                "feature_key": "1",
                "name": "feature_1",
                "enabled": False,
                "value": None,
            },
            "feature_2": {
                "key": "2",
                "feature_key": "2",
                "name": "feature_2",
                "enabled": False,
                "value": None,
            },
        },
        "segments": {
            "1": {
                "key": "1",
                "name": "my_segment",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {"property": "foo", "operator": "EQUAL", "value": "bar"}
                        ],
                        "rules": [],
                    }
                ],
                "overrides": [
                    {
                        "key": "4",
                        "feature_key": "1",
                        "name": "feature_1",
                        "enabled": False,
                        "value": "segment_override",
                        "priority": 2,
                    }
                ],
            },
            "3": {
                "key": "3",
                "name": "higher_priority_segment",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {"property": "foo", "operator": "EQUAL", "value": "bar"}
                        ],
                        "rules": [],
                    }
                ],
                "overrides": [
                    {
                        "enabled": True,
                        "key": "2",
                        "feature_key": "1",
                        "name": "feature_1",
                        "value": "segment_override_other",
                        "priority": 1,
                    }
                ],
            },
        },
    }

    # When
    result = get_evaluation_result(context_in_segments)

    # Then
    assert result == {
        "context": context_in_segments,
        "flags": [
            {
                "enabled": True,
                "feature_key": "1",
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=higher_priority_segment",
                "value": "segment_override_other",
            },
            {
                "enabled": False,
                "feature_key": "2",
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        ],
        "segments": [
            {"key": "1", "name": "my_segment"},
            {"key": "3", "name": "higher_priority_segment"},
        ],
    }


def test_get_evaluation_result__segment_override__no_priority__returns_expected() -> (
    None
):
    # Given
    context: EvaluationContext = {
        "environment": {"key": "api-key", "name": ""},
        "identity": {
            "identifier": "identity_2",
            "key": "api-key_identity_2",
            "traits": {"foo": "bar"},
        },
        "features": {
            "feature_1": {
                "key": "1",
                "feature_key": "1",
                "name": "feature_1",
                "enabled": False,
                "value": None,
            },
            "feature_2": {
                "key": "2",
                "feature_key": "2",
                "name": "feature_2",
                "enabled": False,
                "value": None,
            },
        },
        "segments": {
            "1": {
                "key": "1",
                "name": "segment_without_override_priority",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {"property": "foo", "operator": "EQUAL", "value": "bar"}
                        ],
                        "rules": [],
                    }
                ],
                "overrides": [
                    {
                        "key": "3",
                        "feature_key": "1",
                        "name": "feature_1",
                        "enabled": True,
                        "value": "overridden_without_priority",
                    }
                ],
            },
            "2": {
                "key": "2",
                "name": "segment_with_override_priority",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {"property": "foo", "operator": "EQUAL", "value": "bar"}
                        ],
                        "rules": [],
                    }
                ],
                "overrides": [
                    {
                        "key": "4",
                        "feature_key": "1",
                        "name": "feature_1",
                        "enabled": True,
                        "value": "overridden_with_priority",
                        "priority": 1,
                    }
                ],
            },
            "3": {
                "key": "3",
                "name": "another_segment",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {
                                "property": "$.identity.identifier",
                                "operator": "EQUAL",
                                "value": "identity_2",
                            }
                        ],
                        "rules": [],
                    }
                ],
                "overrides": [
                    {
                        "key": "5",
                        "feature_key": "2",
                        "name": "feature_2",
                        "enabled": False,
                        "value": "moose",
                    }
                ],
            },
        },
    }

    # When
    result = get_evaluation_result(context)

    # Then
    assert result == {
        "context": context,
        "flags": [
            {
                "enabled": True,
                "feature_key": "1",
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=segment_with_override_priority",
                "value": "overridden_with_priority",
            },
            {
                "enabled": False,
                "feature_key": "2",
                "name": "feature_2",
                "reason": "TARGETING_MATCH; segment=another_segment",
                "value": "moose",
            },
        ],
        "segments": [
            {"key": "1", "name": "segment_without_override_priority"},
            {"key": "2", "name": "segment_with_override_priority"},
            {"key": "3", "name": "another_segment"},
        ],
    }
