from unittest import mock

import pytest
from marshmallow import fields

from flag_engine.utils.fields import ListOrDjangoRelatedManagerField

a_list = [1, 2, 3, 4]
mock_related_manager_field = mock.MagicMock()
mock_related_manager_field.filter.return_value = a_list


@pytest.mark.parametrize("attribute", (a_list, mock_related_manager_field))
def test_list_or_django_related_manager_field_serialize(attribute):
    """
    Test to confirm that the custom field serializes the same when given a list
    or a django related manager.
    """

    # Given
    # a dummy object with a single attribute that is defined by the parameterized test
    class MyObject:
        my_attribute = attribute

    my_object = MyObject()

    # and the field we want to test (arbitrarily instantiated with integer elements)
    field = ListOrDjangoRelatedManagerField(fields.Int())

    # When
    # we serialize the attribute on the dummy object
    serialized_data = field.serialize("my_attribute", obj=my_object)

    # Then
    # the result is always outputted the same as the list
    assert serialized_data == a_list


def test_list_or_django_related_manager_field_filter_called_with_correct_arguments():
    # Given
    attribute_name = "my_attribute"
    filters = {"id": None, "another_id__isnull": False}

    # add the spec to the mock to ensure that our mock object only has the relevant
    # attribute this ensures that we can use the mock assertion below instead of having
    # to rely on the response from obj.__getattr__.return_value. See the code for
    # marshmallow.utils.get_value for more information on why.
    object_to_serialize = mock.MagicMock(spec=[attribute_name])
    field = ListOrDjangoRelatedManagerField(
        fields.Int(), metadata={"filter_kwargs": filters}
    )

    # When
    field.serialize(attribute_name, obj=object_to_serialize)

    # Then
    object_to_serialize.my_attribute.filter.assert_called_once_with(**filters)
