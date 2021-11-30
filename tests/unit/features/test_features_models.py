from unittest import mock

import pytest

from flag_engine.features.constants import STANDARD
from flag_engine.features.models import (
    FeatureModel,
    FeatureStateModel,
    MultivariateFeatureOptionModel,
    MultivariateFeatureStateValueModel,
)


def test_feature_state_get_value_no_mv_values(feature_1):
    # Given
    value = "foo"
    feature_state = FeatureStateModel(id=1, feature=feature_1, enabled=True)
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
    mv_feature_option_1 = MultivariateFeatureOptionModel(value=mv_feature_value_1)
    mv_feature_option_2 = MultivariateFeatureOptionModel(value=mv_feature_value_2)

    # and associated values
    mv_feature_state_value_1 = MultivariateFeatureStateValueModel(
        id=1, multivariate_feature_option=mv_feature_option_1, percentage_allocation=30
    )
    mv_feature_state_value_2 = MultivariateFeatureStateValueModel(
        id=2, multivariate_feature_option=mv_feature_option_2, percentage_allocation=30
    )

    # and we assign the above to a feature state
    mv_feature_state = FeatureStateModel(
        id=1,
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
