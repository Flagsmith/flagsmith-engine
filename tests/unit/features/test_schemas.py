from flag_engine.features.schemas import (
    MultivariateFeatureOptionSchema,
    MultivariateFeatureStateValueSchema,
)


def test_can_load_multivariate_feature_option_dict_without_id_field():
    MultivariateFeatureOptionSchema().load({"value": 1})


def test_can_load_multivariate_feature_state_value_without_id_field():
    MultivariateFeatureStateValueSchema().load(
        {
            "multivariate_feature_option": {"value": 1},
            "percentage_allocation": 10,
        }
    )
