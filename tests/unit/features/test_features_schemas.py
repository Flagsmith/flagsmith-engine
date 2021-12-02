import pytest

from flag_engine.features.models import FeatureStateModel
from flag_engine.features.schemas import FeatureStateSchema

feature_state_schema = FeatureStateSchema()


@pytest.mark.parametrize("feature_state_value", ("foo", 1, 1.2, False, True))
def test_feature_state_schema_dump_maintains_correct_value(
    feature_1, feature_state_value
):
    # Given
    feature_state = FeatureStateModel(id=1, feature=feature_1, enabled=True)
    feature_state.set_value(feature_state_value)

    # When
    data = feature_state_schema.dump(feature_state)

    # Then
    assert data["feature_state_value"] == feature_state_value
