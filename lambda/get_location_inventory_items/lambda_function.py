import boto3
import json
from boto3.dynamodb.conditions import Key

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    location_id = int(event["pathParameters"]["id"])

    response = table.query(
        IndexName="location-index",
        KeyConditionExpression=Key("item_location_id").eq(location_id)
    )

    return {
        "statusCode": 200,
        "body": json.dumps(response.get("Items", []))
    }
