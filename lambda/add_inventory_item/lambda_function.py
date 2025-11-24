import boto3
import json
import uuid

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    # Parse request body
    body = json.loads(event["body"])

    # Generate UUID for item_id
    item_id = str(uuid.uuid4())

    new_item = {
        "item_id": item_id,
        "item_name": body["item_name"],
        "item_description": body["item_description"],
        "item_qty_on_hand": int(body["item_qty_on_hand"]),
        "item_price": float(body["item_price"]),
        "location_id": int(body["location_id"])
    }

    # Write item into DynamoDB
    table.put_item(Item=new_item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "item added",
            "item": new_item
        })
    }
