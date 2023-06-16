from unittest import mock

import pytest
from pydantic import ValidationError

from flag_engine.features.constants import STANDARD
from flag_engine.features.models import (
    FeatureModel,
    FeatureStateModel,
    MultivariateFeatureOptionModel,
    MultivariateFeatureStateValueModel,
)
from flag_engine.utils.exceptions import InvalidPercentageAllocation


def test_initializing_feature_state_creates_default_feature_state_uuid(feature_1):
    feature_state = FeatureStateModel(django_id=1, feature=feature_1, enabled=True)
    assert feature_state.featurestate_uuid is not None


def test_initializing_multivariate_feature_state_value_creates_default_uuid():
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
    assert error_data["type"] == "value_error.invalidpercentageallocation"


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
        == "Total percentage allocation for feature must be less than 100 percent"
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
    assert feature_state.multivariate_feature_state_values == [
        mv_fs_value_1,
        mv_fs_value_2,
    ]


def test_feature_state_get_value_no_mv_values(feature_1):
    # Given
    value = "foo"
    feature_state = FeatureStateModel(django_id=1, feature=feature_1, enabled=True)
    feature_state.set_value(value)

    # Then
    # the default value is always returned, even if an identity id is provided
    assert feature_state.get_value() == feature_state.get_value(1) == value


mv_feature_control_value = "control"
mv_feature_value_1 = "foo"
mv_feature_value_2 = "bar"


@pytest.mark.parametrize(
    "percentage_value, expected_value",
    (
        (10, mv_feature_value_1),
        (40, mv_feature_value_2),
        (70, mv_feature_control_value),
    ),
)
@mock.patch("flag_engine.features.models.get_hashed_percentage_for_object_ids")
def test_feature_state_get_value_mv_values(
    mock_get_hashed_percentage, percentage_value, expected_value
):
    # Given
    # a feature
    my_feature = FeatureModel(id=1, name="mv_feature", type=STANDARD)

    # with some multivariate feature options
    mv_feature_option_1 = MultivariateFeatureOptionModel(id=1, value=mv_feature_value_1)
    mv_feature_option_2 = MultivariateFeatureOptionModel(id=2, value=mv_feature_value_2)

    # and associated values
    mv_feature_state_value_1 = MultivariateFeatureStateValueModel(
        id=1, multivariate_feature_option=mv_feature_option_1, percentage_allocation=30
    )
    mv_feature_state_value_2 = MultivariateFeatureStateValueModel(
        id=2, multivariate_feature_option=mv_feature_option_2, percentage_allocation=30
    )

    # and we assign the above to a feature state
    mv_feature_state = FeatureStateModel(
        django_id=1,
        feature=my_feature,
        enabled=True,
        multivariate_feature_state_values=[
            mv_feature_state_value_1,
            mv_feature_state_value_2,
        ],
    )
    mv_feature_state.set_value(mv_feature_control_value)

    # and we mock the function which gets the percentage value for an identity to
    # return a deterministic value so we know which value to expect
    mock_get_hashed_percentage.return_value = percentage_value

    # Then
    # the value of the feature state is correct based on the percentage value returned
    assert mv_feature_state.get_value(identity_id=1) == expected_value


def test_get_value_uses_django_id_for_multivariate_value_calculation_if_not_none(
    feature_1, mv_feature_state_value, mocker
):
    # Given
    mocked_get_hashed_percentage = mocker.patch(
        "flag_engine.features.models.get_hashed_percentage_for_object_ids",
        return_value=10,
    )
    identity_id = 1
    feature_state = FeatureStateModel(
        django_id=1,
        feature=feature_1,
        enabled=True,
        multivariate_feature_state_values=[mv_feature_state_value],
    )
    # When
    feature_state.get_value(identity_id=identity_id)
    # Then
    mocked_get_hashed_percentage.assert_called_with(
        [feature_state.django_id, identity_id]
    )


def test_get_value_uses_featuestate_uuid_for_multivariate_value_calculation_if_django_id_is_not_present(
    feature_1, mv_feature_state_value, mocker
):
    # Given
    mocked_get_hashed_percentage = mocker.patch(
        "flag_engine.features.models.get_hashed_percentage_for_object_ids",
        return_value=10,
    )
    identity_id = 1
    feature_state = FeatureStateModel(
        feature=feature_1,
        enabled=True,
        multivariate_feature_state_values=[mv_feature_state_value],
    )
    # When
    feature_state.get_value(identity_id=identity_id)
    # Then
    mocked_get_hashed_percentage.assert_called_with(
        [feature_state.featurestate_uuid, identity_id]
    )
