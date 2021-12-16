from flag_engine.features.schemas import MultivariateFeatureOptionSchema


def test_can_load_multivariate_feature_option_dict_without_id_field():
    MultivariateFeatureOptionSchema().load({"value": 1})
