import pytest

from flag_engine.context.types import (
    EnvironmentContext,
    EvaluationContext,
    FeatureContext,
    IdentityContext,
    SegmentCondition,
    SegmentContext,
    SegmentRule,
)
from flag_engine.segments import constants


@pytest.fixture()
def segment_condition_property() -> str:
    return "foo"


@pytest.fixture()
def segment_condition_string_value() -> str:
    return "bar"


@pytest.fixture()
def segment_condition(
    segment_condition_property: str,
    segment_condition_string_value: str,
) -> SegmentCondition:
    return {
        "operator": constants.EQUAL,
        "property": segment_condition_property,
        "value": segment_condition_string_value,
    }


@pytest.fixture()
def segment_rule(segment_condition: SegmentCondition) -> SegmentRule:
    return {
        "type": constants.ALL_RULE,
        "conditions": [segment_condition],
    }


@pytest.fixture()
def segment(segment_rule: SegmentRule) -> SegmentContext:
    return {
        "key": "1",
        "name": "my_segment",
        "rules": [segment_rule],
    }


@pytest.fixture()
def feature_state_1() -> FeatureContext:
    return FeatureContext(key="1", name="feature_1", value=None, enabled=True)


@pytest.fixture()
def feature_state_2() -> FeatureContext:
    return FeatureContext(key="2", name="feature_2", value=None, enabled=False)


@pytest.fixture()
def environment() -> EnvironmentContext:
    return EnvironmentContext(
        key="api-key",
        name="Test Environment",
    )


@pytest.fixture()
def identity() -> IdentityContext:
    return IdentityContext(identifier="identity_1", key="api-key_identity_1")


@pytest.fixture
def context(
    environment: EnvironmentContext,
    identity: IdentityContext,
    feature_state_1: FeatureContext,
    feature_state_2: FeatureContext,
    segment: SegmentContext,
) -> EvaluationContext:
    return {
        "environment": environment,
        "features": {
            feature_state_1["name"]: feature_state_1,
            feature_state_2["name"]: feature_state_2,
        },
        "segments": {segment["key"]: segment},
        "identity": identity,
    }


@pytest.fixture()
def identity_in_segment(
    segment_condition_property: str,
    segment_condition_string_value: str,
) -> IdentityContext:
    return IdentityContext(
        identifier="identity_2",
        key="api-key_identity_2",
        traits={
            segment_condition_property: segment_condition_string_value,
        },
    )


@pytest.fixture
def context_in_segment(
    identity_in_segment: IdentityContext,
    context: EvaluationContext,
    segment: SegmentContext,
) -> EvaluationContext:
    return {
        **context,
        "identity": identity_in_segment,
        "segments": {
            segment["key"]: {
                **segment,
                "overrides": [
                    {
                        "key": "4",
                        "name": "feature_1",
                        "enabled": False,
                        "value": "segment_override",
                    }
                ],
            },
        },
    }
