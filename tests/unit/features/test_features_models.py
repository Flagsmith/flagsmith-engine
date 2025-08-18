import pytest
from pydantic import ValidationError

from flag_engine.features.models import (
    FeatureModel,
    FeatureStateModel,
    MultivariateFeatureOptionModel,
    MultivariateFeatureStateValueModel,
)
from flag_engine.utils.exceptions import InvalidPercentageAllocation


def test_initializing_feature_state_creates_default_feature_state_uuid(
    feature_1: FeatureModel,
) -> None:
    feature_state = FeatureStateModel(django_id=1, feature=feature_1, enabled=True)
    assert feature_state.featurestate_uuid is not None


def test_initializing_multivariate_feature_state_value_creates_default_uuid() -> None:
    mv_feature_option = MultivariateFeatureOptionModel(value="value")
    mv_fs_value_model = MultivariateFeatureStateValueModel(
        multivariate_feature_option=mv_feature_option, id=1, percentage_allocation=10
    )
    assert mv_fs_value_model.mv_fs_value_uuid is not None


def test_feature_state_model__invalid_multivariate_feature_state_values__raises_expected(
    feature_1: FeatureModel,
) -> None:
    # Given
    invalid_multivariate_feature_state_values = [
        MultivariateFeatureStateValueModel(
            multivariate_feature_option=MultivariateFeatureOptionModel(value="test"),
            percentage_allocation=50,
        ),
        MultivariateFeatureStateValueModel(
            multivariate_feature_option=MultivariateFeatureOptionModel(value="test2"),
            percentage_allocation=51,
        ),
    ]

    # When
    with pytest.raises(ValidationError) as exc:
        FeatureStateModel(
            feature=feature_1,
            multivariate_feature_state_values=invalid_multivariate_feature_state_values,
            enabled=True,
        )

    # Then
    [error_data] = exc.value.errors()
    assert error_data["loc"] == ("multivariate_feature_state_values",)
    assert error_data["type"] == "value_error"
    assert (
        error_data["msg"]
        == "Value error, Total percentage allocation for feature must be less or equal to 100 percent"
    )


def test_feature_state_model__multivariate_feature_state_values__append_invalid__raises_expected(
    feature_1: FeatureModel,
) -> None:
    # Given
    feature_state = FeatureStateModel(
        feature=feature_1,
        enabled=True,
        multivariate_feature_state_values=[
            MultivariateFeatureStateValueModel(
                multivariate_feature_option=MultivariateFeatureOptionModel(
                    value="test"
                ),
                percentage_allocation=50,
            )
        ],
    )

    # When
    with pytest.raises(InvalidPercentageAllocation) as exc:
        feature_state.multivariate_feature_state_values.append(
            MultivariateFeatureStateValueModel(
                multivariate_feature_option=MultivariateFeatureOptionModel(
                    value="test"
                ),
                percentage_allocation=51,
            )
        )

    # Then
    assert (
        exc.value.args[0]
        == "Total percentage allocation for feature must be less or equal to 100 percent"
    )


def test_feature_state_model__multivariate_feature_state_values__append__expected_result(
    feature_1: FeatureModel,
) -> None:
    # Given
    mv_fs_value_1 = MultivariateFeatureStateValueModel(
        multivariate_feature_option=MultivariateFeatureOptionModel(value="test"),
        percentage_allocation=50,
    )
    mv_fs_value_2 = MultivariateFeatureStateValueModel(
        multivariate_feature_option=MultivariateFeatureOptionModel(value="test"),
        percentage_allocation=30,
    )

    feature_state = FeatureStateModel(
        feature=feature_1,
        enabled=True,
        multivariate_feature_state_values=[mv_fs_value_1],
    )

    # When
    feature_state.multivariate_feature_state_values.append(mv_fs_value_2)

    # Then
    assert list(feature_state.multivariate_feature_state_values) == [
        mv_fs_value_1,
        mv_fs_value_2,
    ]


def test_feature_state_get_value_no_mv_values(feature_1: FeatureModel) -> None:
    # Given
    value = "foo"
    feature_state = FeatureStateModel(django_id=1, feature=feature_1, enabled=True)
    feature_state.set_value(value)

    # Then
    # the default value is always returned, even if an identity id is provided
    assert feature_state.get_value() == feature_state.get_value(1) == value
