from flag_engine.models import Identity, FeatureState, Feature


def test_identity_get_all_feature_states(feature_1, feature_2, environment):
    # Given
    overridden_feature = Feature(id=3, name="overridden_feature")

    # set the state of the feature to False in the environment configuration
    environment.feature_states.append(
        FeatureState(feature=overridden_feature, enabled=False)
    )

    # but True for the identity
    identity = Identity(
        id=1,
        identifier="identity",
        environment_id=environment.id,
        feature_states=[FeatureState(feature=overridden_feature, enabled=True)],
    )

    # When
    all_feature_states = identity.get_all_feature_states(environment=environment)

    # Then
    assert len(all_feature_states) == 3
    for feature_state in all_feature_states:
        environment_feature_state = environment.get_feature_state_for_feature(
            feature_state.feature
        )

        expected = (
            True
            if feature_state.feature == overridden_feature
            else environment_feature_state.enabled
        )
        assert feature_state.enabled is expected
