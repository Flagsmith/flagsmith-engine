from datetime import timedelta
from unittest import mock

import pytest
from marshmallow import fields

from flag_engine.api.fields import (
    APITraitValueField,
    DjangoFeatureStatesRelatedManagerField,
    DjangoRelatedManagerField,
)
from flag_engine.features.constants import STANDARD
from flag_engine.utils.datetime import utcnow_with_tz
from tests.mock_django_classes import DjangoFeature, DjangoFeatureState


@pytest.mark.parametrize(
    "value, deserialized_value",
    (
        ("1", "1"),
        (1.1, 1.1),
        (True, True),
        (-1, -1),
        ({"key": "value"}, str({"key": "value"})),
    ),
)
def test_api_trait_value_field_deserialize(value, deserialized_value):
    field = APITraitValueField()
    assert field.deserialize(value) == deserialized_value


def test_django_related_manager_field_serialize():
    """
    Test to confirm that the custom field serializes the same when given a list
    or a django related manager.
    """

    # Given
    # a mock to represent a related manager object
    a_list = [1, 2, 3, 4]
    mock_related_manager_field = mock.MagicMock()
    mock_related_manager_field.all.return_value = a_list

    # a dummy object with the mock related manager as the only attribute
    class MyObject:
        my_attribute = mock_related_manager_field

    my_object = MyObject()

    # and the field we want to test (arbitrarily instantiated with integer elements)
    field = DjangoRelatedManagerField(fields.Int())

    # When
    # we serialize the attribute on the dummy object
    serialized_data = field.serialize("my_attribute", obj=my_object)

    # Then
    # the result is always outputted the same as the list
    assert serialized_data == a_list


def test_django_related_manager_field_uses_filter_function_as_provided():
    # Given
    attribute_name = "my_attribute"

    # add the spec to the mock to ensure that our mock object only has the relevant
    # attribute this ensures that we can use the mock assertion below instead of having
    # to rely on the response from obj.__getattr__.return_value. See the code for
    # marshmallow.utils.get_value for more information on why.
    object_to_serialize = mock.MagicMock(spec=[attribute_name])

    object_to_serialize.my_attribute.all.return_value = [1, 2, 3, 4]

    def filter_func(e):
        return e > 2

    field = DjangoRelatedManagerField(fields.Int(), filter_func=filter_func)

    # When
    serialized_data = field.serialize(attribute_name, obj=object_to_serialize)

    # Then
    object_to_serialize.my_attribute.all.assert_called_once()
    assert serialized_data == [3, 4]


def test_django_feature_state_related_manager_field_serialize_discards_old_versions(
    django_project,
):
    # Given
    # a mock object to serialize
    attribute_name = "feature_states"
    object_to_serialize = mock.MagicMock(spec=[attribute_name])

    # and which has some 'feature states' associated with it in the way that you'd
    # expect a django object to. Each feature state associated with the same feature
    # but with incrementing version numbers.
    yesterday = utcnow_with_tz() - timedelta(days=1)

    def gt_mock_side_effect(first, second):
        # Simplified version of FeatureState.__gt__ from the django project.
        return first.live_from < utcnow_with_tz() and (
            first.live_from > second.live_from or first.version > second.version
        )

    django_feature = DjangoFeature(
        id=1, name="test_feature", project=django_project, type=STANDARD
    )

    feature_states = []
    for i in range(1, 6):
        mock_fs = DjangoFeatureState(
            id=i,
            feature=django_feature,
            version=i,
            live_from=yesterday,
            enabled=True,
            gt_mock=mock.MagicMock(side_effect=gt_mock_side_effect),
        )
        feature_states.append(mock_fs)

    getattr(object_to_serialize, attribute_name).all.return_value = feature_states

    # and a filter function which will filter out the last feature state based on it's
    # id
    def filter_func(fs):
        return fs.id < 5

    # and we instantiate the field to test against
    field = DjangoFeatureStatesRelatedManagerField(
        fields.Field(), filter_func=filter_func
    )

    # When
    # we serialize the field holding the feature states
    serialized_data = field.serialize(attribute_name, obj=object_to_serialize)

    # Then
    # the 'feature states' were retrieved as expected
    getattr(object_to_serialize, attribute_name).all.assert_called_once()

    # and only one 'feature state' is returned which has an id and version of 4 (because
    # it's the maximum version that was not filtered out by the filter function).
    assert len(serialized_data) == 1
    assert serialized_data[0].id == serialized_data[0].version == 4
