import boto3
import json
import ulid

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    body = json.loads(event["body"])

    new_item = {
        "item_id": str(ulid.new()),
        "item_name": body["item_name"],
        "item_description": body["item_description"],
        "item_qty_on_hand": int(body["item_qty_on_hand"]),
        "item_price": float(body["item_price"]),
        "item_location_id": int(body["item_location_id"])
    }

    table.put_item(Item=new_item)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "item added", "item": new_item})
    }
