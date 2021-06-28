from unittest import mock

import pytest
from marshmallow import fields

from flag_engine.fields import ListOrDjangoRelatedManagerField

a_list = [1, 2, 3, 4]
mock_related_manager_field = mock.MagicMock()
mock_related_manager_field.all.return_value = a_list


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
