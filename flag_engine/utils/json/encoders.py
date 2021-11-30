import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    """
    Convert decimal to int/float because decimals are nothing but
    int/float(for us) converted to decimal by boto3/dynamodb.
    """

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return json.JSONEncoder.default(self, obj)
