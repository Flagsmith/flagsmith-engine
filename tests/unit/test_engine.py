import json
from typing import TYPE_CHECKING, TypedDict

if not TYPE_CHECKING:
    # `reveal_type` is a pseudo-builtin only available when type checking.
    # Define a no-op version here so that we can call it in the tests.
    def reveal_type(x: object) -> None: ...


from flag_engine.context.types import EvaluationContext, IdentityContext, SegmentContext
from flag_engine.engine import get_evaluation_result
from flag_engine.result.types import EvaluationResult


def test_get_evaluation_result__no_overrides__returns_expected(
    context: EvaluationContext,
) -> None:
    # When
    result = get_evaluation_result(context)

    # Then
    assert result == EvaluationResult(
        flags={
            "feature_1": {
                "enabled": True,
                "name": "feature_1",
                "reason": "DEFAULT",
                "value": None,
            },
            "feature_2": {
                "enabled": False,
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        },
        segments=[],
    )


def test_get_evaluation_result__segment_override__returns_expected(
    context_in_segment: EvaluationContext,
) -> None:
    # When
    result = get_evaluation_result(context_in_segment)

    # Then
    assert result == {
        "flags": {
            "feature_1": {
                "enabled": False,
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=my_segment",
                "value": "segment_override",
            },
            "feature_2": {
                "enabled": False,
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        },
        "segments": [{"name": "my_segment"}],
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
        "flags": {
            "feature_1": {
                "enabled": True,
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=identity_overrides",
                "value": "overridden_for_identity",
            },
            "feature_2": {
                "enabled": False,
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        },
        "segments": [{"name": "identity_overrides"}],
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
                "name": "feature_1",
                "enabled": False,
                "value": None,
            },
            "feature_2": {
                "key": "2",
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
        "flags": {
            "feature_1": {
                "enabled": True,
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=higher_priority_segment",
                "value": "segment_override_other",
            },
            "feature_2": {
                "enabled": False,
                "name": "feature_2",
                "reason": "DEFAULT",
                "value": None,
            },
        },
        "segments": [
            {"name": "my_segment"},
            {"name": "higher_priority_segment"},
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
                "name": "feature_1",
                "enabled": False,
                "value": None,
            },
            "feature_2": {
                "key": "2",
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
        "flags": {
            "feature_1": {
                "enabled": True,
                "name": "feature_1",
                "reason": "TARGETING_MATCH; segment=segment_with_override_priority",
                "value": "overridden_with_priority",
            },
            "feature_2": {
                "enabled": False,
                "name": "feature_2",
                "reason": "TARGETING_MATCH; segment=another_segment",
                "value": "moose",
            },
        },
        "segments": [
            {"name": "segment_without_override_priority"},
            {"name": "segment_with_override_priority"},
            {"name": "another_segment"},
        ],
    }


def test_segment_metadata_generic_type__returns_expected() -> None:
    # Given
    class CustomSegmentMetadata(TypedDict):
        foo: str
        bar: int

    segment_metadata = CustomSegmentMetadata(foo="hello", bar=123)

    evaluation_context: EvaluationContext[CustomSegmentMetadata] = {
        "environment": {"key": "api-key", "name": ""},
        "segments": {
            "1": {
                "key": "1",
                "name": "my_segment",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {
                                "property": "$.environment.name",
                                "operator": "EQUAL",
                                "value": "",
                            }
                        ],
                        "rules": [],
                    }
                ],
                "metadata": segment_metadata,
            },
        },
    }

    # When
    result = get_evaluation_result(evaluation_context)

    # Then
    assert result["segments"][0]["metadata"] is segment_metadata
    reveal_type(result["segments"][0]["metadata"])  # CustomSegmentMetadata


def test_segment_metadata_generic_type__default__returns_expected() -> None:
    # Given
    segment_metadata = {"hello": object()}

    # we don't specify generic type, but mypy is happy with this
    evaluation_context: EvaluationContext = {
        "environment": {"key": "api-key", "name": ""},
        "segments": {
            "1": {
                "key": "1",
                "name": "my_segment",
                "rules": [
                    {
                        "type": "ALL",
                        "conditions": [
                            {
                                "property": "$.environment.name",
                                "operator": "EQUAL",
                                "value": "",
                            }
                        ],
                        "rules": [],
                    }
                ],
                "metadata": segment_metadata,
            },
        },
    }

    # When
    result = get_evaluation_result(evaluation_context)

    # Then
    assert result["segments"][0]["metadata"] is segment_metadata
    reveal_type(result["segments"][0]["metadata"])  # Mapping[str, object]


def test_feature_metadata_generic_type__returns_expected() -> None:
    # Given
    class CustomFeatureMetadata(TypedDict):
        foo: str
        bar: int

    feature_metadata = CustomFeatureMetadata(foo="hello", bar=123)

    evaluation_context: EvaluationContext[None, CustomFeatureMetadata] = {
        "environment": {"key": "api-key", "name": ""},
        "features": {
            "feature_1": {
                "key": "1",
                "name": "feature_1",
                "enabled": False,
                "value": None,
                "metadata": feature_metadata,
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
                            {
                                "property": "$.environment.name",
                                "operator": "EQUAL",
                                "value": "",
                            }
                        ],
                        "rules": [],
                    }
                ],
                "overrides": [
                    {
                        "key": "5",
                        "name": "feature_1",
                        "enabled": True,
                        "value": "overridden_for_identity",
                        "metadata": feature_metadata,
                    }
                ],
            },
        },
    }

    # When
    result = get_evaluation_result(evaluation_context)

    # Then
    assert result["flags"]["feature_1"]["metadata"] is feature_metadata
    reveal_type(result["flags"]["feature_1"]["metadata"])  # CustomFeatureMetadata


def test_feature_metadata_generic_type__default__returns_expected() -> None:
    # Given
    feature_metadata = {"hello": object()}

    # we don't specify generic type, but mypy is happy with this
    evaluation_context: EvaluationContext = {
        "environment": {"key": "api-key", "name": ""},
        "features": {
            "feature_1": {
                "key": "1",
                "name": "feature_1",
                "enabled": False,
                "value": None,
                "metadata": feature_metadata,
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
                            {
                                "property": "$.environment.name",
                                "operator": "EQUAL",
                                "value": "",
                            }
                        ],
                        "rules": [],
                    }
                ],
                "overrides": [
                    {
                        "key": "5",
                        "name": "feature_1",
                        "enabled": True,
                        "value": "overridden_for_identity",
                        "metadata": feature_metadata,
                    }
                ],
            },
        },
    }

    # When
    result = get_evaluation_result(evaluation_context)

    # Then
    assert result["flags"]["feature_1"]["metadata"] is feature_metadata
    reveal_type(result["flags"]["feature_1"]["metadata"])  # Mapping[str, object]
