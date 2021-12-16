from unittest import mock

import pytest

from flag_engine.features.constants import MULTIVARIATE, STANDARD
from flag_engine.features.models import (
    FeatureModel,
    FeatureStateModel,
    MultivariateFeatureOptionModel,
    MultivariateFeatureStateValueModel,
)


def test_initializing_feature_state_creates_default_feature_state_uuid(feature_1):
    feature_state = FeatureStateModel(django_id=1, feature=feature_1, enabled=True)
    assert feature_state.featurestate_uuid is not None


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


def test_identity_gets_same_mv_feature_on_multiple_requests(identity):
    """
    Test to confirm that, given a fixed set of variables, a given identity receives
    the same value for a multivariate feature on all requests.
    """

    # Given
    mv_feature = FeatureModel(id=3, name="mv_feature", type=MULTIVARIATE)

    mv_values = []
    for id_, value, percentage_allocation in (
        (1, "foo", 30),
        (2, "bar", 30),
        (3, "baz", 40),
    ):
        mv_option = MultivariateFeatureOptionModel(value=value)
        mv_feature_state_value_1 = MultivariateFeatureStateValueModel(
            id=id_,
            multivariate_feature_option=mv_option,
            percentage_allocation=percentage_allocation,
        )
        mv_values.append(mv_feature_state_value_1)

    mv_feature_state = FeatureStateModel(
        feature=mv_feature,
        featurestate_uuid="203a50e3-b6ad-44b4-b0b9-03b29db5cc8a",
        django_id=78986,
        enabled=True,
        multivariate_feature_state_values=mv_values,
    )

    # When
    values = [mv_feature_state.get_value(identity.identifier) for _ in range(50)]

    # Then
    assert len(set(values)) == 1
    assert values[0] == "foo"
