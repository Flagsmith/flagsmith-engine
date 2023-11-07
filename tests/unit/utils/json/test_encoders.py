import json
from decimal import Decimal

import pytest
from pytest_mock import MockerFixture

from flag_engine.utils.json.encoders import DecimalEncoder


def test_decimal_encoder_converts_decimal() -> None:
    # Given
    data = {
        "int_decimal": Decimal(1),
        "float_decimal": Decimal("1.99"),
        "str_value": "string",
    }

    # when
    json_data = json.loads(json.dumps(data, cls=DecimalEncoder))

    # Then
    assert isinstance(json_data["int_decimal"], int)
    assert isinstance(json_data["float_decimal"], float)
    assert isinstance(json_data["str_value"], str)

    assert json_data == {
        "int_decimal": 1,
        "float_decimal": 1.99,
        "str_value": "string",
    }


def test_decimal_encoder__invalid_value__fallback_expected(
    mocker: MockerFixture,
) -> None:
    # Given
    encoder_default_mock = mocker.patch(
        "flag_engine.utils.json.encoders.json.JSONEncoder.default",
        side_effect=ValueError,
    )
    invalid_data = object()
    data = {"invalid": invalid_data}

    # When
    with pytest.raises(ValueError):
        json.dumps(data, cls=DecimalEncoder)

    # Then
    encoder_default_mock.assert_called_once_with(mocker.ANY, invalid_data)
