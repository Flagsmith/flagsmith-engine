import pytest

from flag_engine.utils.exceptions import FeatureStateNotFound


def test_environment_get_feature_state_raises_exception_if_feature_is_missing(
    environment,
):
    with pytest.raises(FeatureStateNotFound):
        environment.get_feature_state(feature_name="that_feature_does_not_exists")


def test_environment_get_feature_state_returns_correct_feature_state(
    environment, feature_1
):
    # When
    fs = environment.get_feature_state(feature_1.name)
    # Then
    assert fs.feature == feature_1
