import pytest

from flag_engine.features.models import FeatureStateModel
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
    updated_traits = identity_in_segment.update_traits([trait_to_remove])

    # Then
    assert identity_in_segment.identity_traits == updated_traits == []


def test_update_identity_traits_updates_trait_value(identity_in_segment):
    # Given
    trait_key = identity_in_segment.identity_traits[0].trait_key
    trait_value = "updated_trait_value"
    trait_to_update = TraitModel(trait_key=trait_key, trait_value=trait_value)

    # When
    updated_traits = identity_in_segment.update_traits([trait_to_update])

    # Then
    assert updated_traits == identity_in_segment.identity_traits
    assert len(identity_in_segment.identity_traits) == 1
    assert identity_in_segment.identity_traits[0] == trait_to_update


def test_update_traits_adds_new_traits(identity_in_segment):
    # Given
    new_trait = TraitModel(trait_key="new_key", trait_value="foobar")

    # When
    updated_traits = identity_in_segment.update_traits([new_trait])

    # Then
    assert updated_traits == identity_in_segment.identity_traits
    assert len(identity_in_segment.identity_traits) == 2
    assert new_trait in identity_in_segment.identity_traits


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


def test_append_feature_state(identity, feature_1):
    # Given
    fs_1 = FeatureStateModel(feature=feature_1, enabled=False)
    # When
    identity.identity_features.append(fs_1)
    # Then
    fs_1 in identity.identity_features
