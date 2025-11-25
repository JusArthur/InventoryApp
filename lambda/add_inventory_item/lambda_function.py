import boto3
import json
import uuid
from decimal import Decimal

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    print("EVENT:", event)  # Debug

    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        elif body is None:
            body = {}

        new_item = {
            "item_id": str(uuid.uuid4()),
            "item_name": body.get("item_name", ""),
            "item_description": body.get("item_description", ""),
            "item_qty_on_hand": int(body.get("item_qty_on_hand", 0)),
            "item_price": Decimal(str(body.get("item_price", 0))),
            "location_id": int(body.get("location_id", 0))
        }

        table.put_item(Item=new_item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "item added", "item": new_item}, default=str)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error", "error": str(e)})
        }
