import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    try:
        location_id = int(event["pathParameters"]["id"])  # if stored as number; remove int() if string

        response = table.query(
            IndexName="location-index",  # make sure this GSI exists on 'location_id'
            KeyConditionExpression=Key("location_id").eq(location_id)
        )

        items = response.get("Items", [])

        # Convert Decimal to float for JSON
        def convert_decimal(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError

        return {
            "statusCode": 200,
            "body": json.dumps(items, default=convert_decimal)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error",
                "error": str(e)
            })
        }
