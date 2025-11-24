import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key

table = boto3.resource('dynamodb').Table('Inventory')

def decimal_to_native(obj):
    if isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    raise TypeError

def lambda_handler(event, context):
    try:
        item_id = event.get("pathParameters", {}).get("id")

        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing item_id in path"})
            }

        # Query by PK only
        response = table.query(
            KeyConditionExpression=Key("item_id").eq(item_id)
        )

        items = response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Item not found"})
            }

        # Return first match
        return {
            "statusCode": 200,
            "body": json.dumps(items[0], default=decimal_to_native)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
