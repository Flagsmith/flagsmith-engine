import pytest

from flag_engine.identities.models import IdentityModel, TraitModel
from flag_engine.segments.evaluator import evaluate_identity_in_segment

from .fixtures import (
    empty_segment,
    segment_conditions_and_nested_rules,
    segment_multiple_conditions_all,
    segment_multiple_conditions_any,
    segment_nested_rules,
    segment_single_condition,
    trait_key_1,
    trait_key_2,
    trait_key_3,
    trait_value_1,
    trait_value_2,
    trait_value_3,
)


@pytest.mark.parametrize(
    "segment, identity_traits, expected_result",
    (
        (empty_segment, [], False),
        (segment_single_condition, [], False),
        (
            segment_single_condition,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            True,
        ),
        (segment_multiple_conditions_all, [], False),
        (
            segment_multiple_conditions_all,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            False,
        ),
        (
            segment_multiple_conditions_all,
            [
                TraitModel(trait_key=trait_key_1, trait_value=trait_value_1),
                TraitModel(trait_key=trait_key_2, trait_value=trait_value_2),
            ],
            True,
        ),
        (segment_multiple_conditions_any, [], False),
        (
            segment_multiple_conditions_any,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            True,
        ),
        (
            segment_multiple_conditions_any,
            [TraitModel(trait_key=trait_key_2, trait_value=trait_value_2)],
            True,
        ),
        (
            segment_multiple_conditions_any,
            [
                TraitModel(trait_key=trait_key_1, trait_value=trait_value_1),
                TraitModel(trait_key=trait_key_2, trait_value=trait_value_2),
            ],
            True,
        ),
        (segment_nested_rules, [], False),
        (
            segment_nested_rules,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            False,
        ),
        (
            segment_nested_rules,
            [
                TraitModel(trait_key=trait_key_1, trait_value=trait_value_1),
                TraitModel(trait_key=trait_key_2, trait_value=trait_value_2),
                TraitModel(trait_key=trait_key_3, trait_value=trait_value_3),
            ],
            True,
        ),
        (segment_conditions_and_nested_rules, [], False),
        (
            segment_conditions_and_nested_rules,
            [TraitModel(trait_key=trait_key_1, trait_value=trait_value_1)],
            False,
        ),
        (
            segment_conditions_and_nested_rules,
            [
                TraitModel(trait_key=trait_key_1, trait_value=trait_value_1),
                TraitModel(trait_key=trait_key_2, trait_value=trait_value_2),
                TraitModel(trait_key=trait_key_3, trait_value=trait_value_3),
            ],
            True,
        ),
    ),
)
def test_identity_in_segment(segment, identity_traits, expected_result):
    identity = IdentityModel(
        identifier="foo",
        identity_traits=identity_traits,
        environment_api_key="api-key",
    )

    assert evaluate_identity_in_segment(identity, segment) == expected_result
