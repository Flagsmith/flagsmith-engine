def test_environment_feature_states(environment_with_segment_override):
    # When
    environment_feature_states = environment_with_segment_override.feature_states

    # Then
    assert len(environment_feature_states) == 2
    assert all(
        not fs.segment_id and not fs.identity_id for fs in environment_feature_states
    )


def test_environment_segment_overrides(
    environment_with_segment_override, segment_override_fs
):
    # When
    segment_overrides = environment_with_segment_override.segment_overrides

    # Then
    assert len(segment_overrides) == 1
    assert segment_overrides[0] == segment_override_fs
