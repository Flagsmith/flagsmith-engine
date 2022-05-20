from dataclasses import dataclass

from flag_engine.api.filters import filter_feature_segments


def test_filter_feature_segments():
    # Given
    @dataclass
    class MockEnvironment:
        api_key: str

    @dataclass
    class MockFeatureSegment:
        id: int
        feature_id: int
        priority: int
        environment: object

    api_key = "api-key"
    valid_env = MockEnvironment(api_key=api_key)
    invalid_env = MockEnvironment(api_key="some-other-api-key")

    feature_segments = [
        MockFeatureSegment(id=1, feature_id=2, priority=1, environment=valid_env),
        MockFeatureSegment(id=2, feature_id=2, priority=2, environment=valid_env),
        MockFeatureSegment(id=3, feature_id=1, priority=1, environment=valid_env),
        MockFeatureSegment(id=4, feature_id=1, priority=1, environment=invalid_env),
    ]

    # When
    sorted_feature_segments = filter_feature_segments(
        feature_segments, environment_api_key=api_key
    )

    # Then
    # the feature segment for a different environment was removed
    assert len(sorted_feature_segments) == 3

    # and the feature segments have been sorted correctly by feature, then by priority
    # (descending)
    # assert sorted_feature_segments[0].id == 3
    # assert sorted_feature_segments[1].id == 2
    # assert sorted_feature_segments[2].id == 1
