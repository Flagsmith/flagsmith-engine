from flag_engine.identities.models import IdentityModel, TraitModel


def test_composite_key():
    # Given
    environment_api_key = "abc123"
    identifier = "identity"
    identity_model = IdentityModel(
        environment_api_key=environment_api_key, identifier=identifier
    )

    # Then
    assert identity_model.composite_key == f"{environment_api_key}_{identifier}"


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
    identity_in_segment.update_traits([trait_to_remove])

    # Then
    assert identity_in_segment.identity_traits == []


def test_update_identity_traits_updates_trait_value(identity_in_segment):
    # Given
    trait_key = identity_in_segment.identity_traits[0].trait_key
    trait_value = "updated_trait_value"
    trait_to_update = TraitModel(trait_key=trait_key, trait_value=trait_value)

    # When
    identity_in_segment.update_traits([trait_to_update])

    # Then
    assert len(identity_in_segment.identity_traits) == 1
    assert identity_in_segment.identity_traits[0] == trait_to_update


def test_update_traits_adds_new_traits(identity_in_segment):
    # Given
    new_trait = TraitModel(trait_key="new_key", trait_value="foobar")

    # When
    identity_in_segment.update_traits([new_trait])

    # Then
    assert len(identity_in_segment.identity_traits) == 2
    assert new_trait in identity_in_segment.identity_traits
