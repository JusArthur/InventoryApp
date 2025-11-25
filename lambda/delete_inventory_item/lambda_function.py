import boto3
import json
from decimal import Decimal

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    item_id = event.get("pathParameters", {}).get("id")

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

        # Delete each item
        for item in items:
            table.delete_item(
                Key={
                    "item_id": item["item_id"],
                    "item_location_id": item["item_location_id"]
                }
            )

        # Convert Decimals to float for JSON serialization
        def convert_decimal(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Deleted {len(items)} item(s) with item_id {item_id}",
                "deleted_items": items
            }, default=convert_decimal)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error", "error": str(e)})
        }
