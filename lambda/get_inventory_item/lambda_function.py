import boto3
import json
from decimal import Decimal

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    path_params = event.get("pathParameters", {})
    item_id = path_params.get("id")  # only partition key needed

    if not item_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing item_id in path"})
        }

    try:
        # Query all items with this partition key
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('item_id').eq(item_id)
        )

        items = response.get("Items", [])

        # Convert Decimal to str for JSON
        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return str(obj)
            raise TypeError

        return {
            "statusCode": 200,
            "body": json.dumps(items, default=decimal_default)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error", "error": str(e)})
        }
