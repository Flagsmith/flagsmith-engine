import json
from decimal import Decimal
from flag_engine.utils.json.encoders import DecimalEncoder


def test_decimal_encoder_converts_decimal():
    # Given
    data = {"int_decimal": Decimal(1), "float_decimal": Decimal("1.99"), "str_value": "string"}

    # when
    json_data = json.dumps(data, cls=DecimalEncoder)

    # Then
    assert json.loads(json_data) == {"int_decimal": 1, "float_decimal": 1.99, "str_value": "string"}


