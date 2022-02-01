from dataclasses import dataclass

from flag_engine.django_transform.filters import sort_and_filter_feature_segments


def test_sort_and_filter_feature_segments():
    # Given
    @dataclass
    class MockEnvironment:
        api_key: str

    @dataclass
    class MockFeatureSegment:
        id: int
        feature: int
        priority: int
        environment: object

    api_key = "api-key"
    matching_env = MockEnvironment(api_key=api_key)
    not_matching_env = MockEnvironment(api_key="some-other-api-key")

    feature_segments = [
        MockFeatureSegment(id=1, feature=2, priority=1, environment=matching_env),
        MockFeatureSegment(id=2, feature=2, priority=2, environment=matching_env),
        MockFeatureSegment(id=3, feature=1, priority=1, environment=matching_env),
        MockFeatureSegment(id=4, feature=1, priority=1, environment=not_matching_env),
    ]

    # When
    sorted_feature_segments = sort_and_filter_feature_segments(
        feature_segments, environment_api_key=api_key
    )

    # Then
    # the feature segment for a different environment was removed
    assert len(sorted_feature_segments) == 3

    # and the feature segments have been sorted correctly by feature, then by priority
    # (descending)
    assert sorted_feature_segments[0].id == 3
    assert sorted_feature_segments[1].id == 2
    assert sorted_feature_segments[2].id == 1
