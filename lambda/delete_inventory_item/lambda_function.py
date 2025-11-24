import boto3
import json
from boto3.dynamodb.conditions import Key

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    item_id = event["pathParameters"]["id"]

    # Query all items with this item_id
    response = table.query(
        KeyConditionExpression=Key("item_id").eq(item_id)
    )

    items = response.get("Items", [])

    if not items:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "No items found with this item_id"})
        }

    # Delete each item
    for item in items:
        table.delete_item(
            Key={
                "item_id": item["item_id"],
                "location_id": item["location_id"]  # SK required
            }
        )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Deleted {len(items)} item(s) with item_id {item_id}"
        })
    }
