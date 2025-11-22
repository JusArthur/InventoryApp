import boto3
import json
from boto3.dynamodb.conditions import Key

table = boto3.resource('dynamodb').Table('Inventory')

def lambda_handler(event, context):
    response = table.scan()
    return {
        "statusCode": 200,
        "body": json.dumps(response.get("Items", []))
    }

