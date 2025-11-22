import boto3
import json

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    item_id = event["pathParameters"]["id"]

    table.delete_item(Key={"item_id": item_id})

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "item deleted", "id": item_id})
    }
