from typing import Any
import pytest

from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.utils.exceptions import DuplicateFeatureState


def test_composite_key():
    # Given
    environment_api_key = "abc123"
    identifier = "identity"

    identity_model = IdentityModel(
        environment_api_key=environment_api_key, identifier=identifier
    )

    # Then
    assert identity_model.composite_key == f"{environment_api_key}_{identifier}"


def test_identiy_model_creates_default_identity_uuid():
    identity_model = IdentityModel(identifier="test", environment_api_key="some_key")
    assert identity_model.identity_uuid is not None


def test_generate_composite_key():
    # Given
    environment_api_key = "abc123"
    identifier = "identity"

    # Then
    assert (
        IdentityModel.generate_composite_key(
            env_key=environment_api_key, identifier=identifier
        )
        == f"{environment_api_key}_{identifier}"
    )


def test_update_traits_remove_traits_with_none_value(identity_in_segment):
    # Given
    trait_key = identity_in_segment.identity_traits[0].trait_key
    trait_to_remove = TraitModel(trait_key=trait_key, trait_value=None)

    # When
    updated_traits, traits_updated = identity_in_segment.update_traits(
        [trait_to_remove]
    )

    # Then
    assert identity_in_segment.identity_traits == updated_traits == []
    assert traits_updated is True


def test_update_identity_traits_updates_trait_value(identity_in_segment):
    # Given
    trait_key = identity_in_segment.identity_traits[0].trait_key
    trait_value = "updated_trait_value"
    trait_to_update = TraitModel(trait_key=trait_key, trait_value=trait_value)

    # When
    updated_traits, traits_updated = identity_in_segment.update_traits(
        [trait_to_update]
    )

    # Then
    assert updated_traits == identity_in_segment.identity_traits
    assert len(identity_in_segment.identity_traits) == 1
    assert identity_in_segment.identity_traits[0] == trait_to_update
    assert traits_updated is True


def test_update_traits_adds_new_traits(identity_in_segment):
    # Given
    new_trait = TraitModel(trait_key="new_key", trait_value="foobar")

    # When
    updated_traits, traits_updated = identity_in_segment.update_traits([new_trait])

    # Then
    assert updated_traits == identity_in_segment.identity_traits
    assert len(identity_in_segment.identity_traits) == 2
    assert new_trait in identity_in_segment.identity_traits
    assert traits_updated is True


def test_update_traits_returns_false_if_traits_are_not_updated(identity_in_segment):
    # Given
    trait_key = identity_in_segment.identity_traits[0].trait_key
    trait_value = identity_in_segment.identity_traits[0].trait_value

    trait_to_update = TraitModel(trait_key=trait_key, trait_value=trait_value)

    # When
    updated_traits, traits_updated = identity_in_segment.update_traits(
        [trait_to_update]
    )

    # Then
    assert updated_traits == identity_in_segment.identity_traits
    assert len(identity_in_segment.identity_traits) == 1
    assert identity_in_segment.identity_traits[0] == trait_to_update
    assert traits_updated is False


def test_appending_feature_states_raises_duplicate_feature_state_if_fs_for_the_feature_already_exists(
    identity, feature_1
):
    # Given
    fs_1 = FeatureStateModel(feature=feature_1, enabled=False)
    fs_2 = FeatureStateModel(feature=feature_1, enabled=True)
    identity.identity_features.append(fs_1)

    # Then
    with pytest.raises(DuplicateFeatureState):
        identity.identity_features.append(fs_2)


def test_identity_model__identity_features__append__expected_result(
    identity: IdentityModel,
    feature_1: FeatureModel,
    feature_2: FeatureModel,
) -> None:
    # Given
    fs_1 = FeatureStateModel(feature=feature_1, enabled=False)
    fs_2 = FeatureStateModel(feature=feature_2, enabled=True)
    identity.identity_features.append(fs_1)

    # When
    identity.identity_features.append(fs_2)

    # Then
    assert identity.identity_features == [
        fs_1,
        fs_2,
    ]


def test_append_feature_state(identity, feature_1):
    # Given
    fs_1 = FeatureStateModel(feature=feature_1, enabled=False)
    # When
    identity.identity_features.append(fs_1)
    # Then
    fs_1 in identity.identity_features


def test_prune_features_only_keeps_valid_features(
    identity, feature_state_1, feature_state_2
):
    # Given
    identity.identity_features.append(feature_state_1)
    identity.identity_features.append(feature_state_2)

    valid_features = [feature_state_1.feature.name]

    # When
    identity.prune_features(valid_features)

    # Then
    assert identity.identity_features == [feature_state_1]


def test_get_hash_key_with_use_identity_composite_key_for_hashing_enabled(identity):
    assert (
        identity.get_hash_key(use_identity_composite_key_for_hashing=True)
        == identity.composite_key
    )


def test_get_hash_key_with_use_identity_composite_key_for_hashing_disabled(identity):
    assert (
        identity.get_hash_key(use_identity_composite_key_for_hashing=False)
        == identity.identifier
    )


@pytest.mark.parametrize(
    "trait_value, expected_result",
    [
        (True, True),
        (1.0, 1.0),
        (1, 1),
        (False, False),
        (0.0, 0.0),
        (0, 0),
    ],
)
def test_trait_model__deserialize__expected_trait_value(
    trait_value: Any,
    expected_result: Any,
) -> None:
    # When
    result = TraitModel.parse_obj({"trait_key": "test", "trait_value": trait_value})

    # Then
    assert isinstance(result.trait_value, type(expected_result))
    assert result.trait_value == expected_result
