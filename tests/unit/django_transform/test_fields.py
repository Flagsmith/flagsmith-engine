from unittest import mock

from marshmallow import fields

from flag_engine.django_transform.fields import DjangoRelatedManagerField


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
