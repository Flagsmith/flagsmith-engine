import pytest

from flag_engine.features.models import FeatureModel, FeatureStateModel
from flag_engine.features.schemas import (
    FeatureStateSchema,
    MultivariateFeatureOptionSchema,
    MultivariateFeatureStateValueSchema,
)
from flag_engine.utils.exceptions import InvalidPercentageAllocation


def test_can_load_multivariate_feature_option_dict_without_id_field():
    MultivariateFeatureOptionSchema().load({"value": 1})


def test_can_load_multivariate_feature_state_value_without_id_field():
    MultivariateFeatureStateValueSchema().load(
        {
            "multivariate_feature_option": {"value": 1},
            "percentage_allocation": 10,
        }
    )


def test_dumping_fs_schema_raises_invalid_percentage_allocation_for_invalid_allocation():
    # Given
    data = {
        "multivariate_feature_state_values": [
            {"multivariate_feature_option": 12, "percentage_allocation": 100},
            {"multivariate_feature_option": 9, "percentage_allocation": 80},
        ],
        "feature_state_value": "value",
    }
    # Then
    with pytest.raises(InvalidPercentageAllocation):
        FeatureStateSchema().dump(data)


def test_dumping_fs_schema_works_for_valid_allocation():
    # Given
    data = {
        "multivariate_feature_state_values": [
            {"multivariate_feature_option": 12, "percentage_allocation": 20},
            {"multivariate_feature_option": 9, "percentage_allocation": 80},
        ],
        "feature_state_value": "value",
    }
    # Then
    FeatureStateSchema().dump(data)


def test_can_dump_featurestate_schema_without_mvfs(feature_1):
    # Given
    raw_data = {"feature_state_value": "value"}
    # When
    dumped_data = FeatureStateSchema(
        exclude=["multivariate_feature_state_values"]
    ).dump(raw_data)
    # Then
    assert raw_data["feature_state_value"] == dumped_data["feature_state_value"]


def test_dumping_feature_state_model_returns_dict_with_feature_state_value():
    # Given
    feature = FeatureModel(id=1, name="test_feature", type="STANDARD")
    fs_value = "some_value"
    fs_model = FeatureStateModel(feature=feature, enabled=True)
    # When
    fs_model.set_value(fs_value)
    # Then
    assert FeatureStateSchema().dump(fs_model)["feature_state_value"] == fs_value
