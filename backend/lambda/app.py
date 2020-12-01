from __future__ import print_function
import os
import json

import boto3
from botocore.exceptions import ClientError

# Default config vals
DYNAMODB_TABLE_NAME = os.environ['SIGNUP_TABLE']
SNS_TOPIC = os.environ['NEW_SIGNUP_TOPIC']
DEBUG = os.environ.get('FLASK_DEBUG') in ['true', 'True']

# Connect to DynamoDB and get ref to Table
DYNAMODB = boto3.resource('dynamodb')
DDB_TABLE = DYNAMODB.Table(DYNAMODB_TABLE_NAME)

# Connect to SNS
SNS = boto3.client('sns')

def signup(event, context):

    if DEBUG:
        print("[DEBUG] Signup with body: %s" % event['body'])
        print("[DEBUG] Event: %s" % json.dumps(event))
        print("[DEBUG] Context: %s" % json.dumps(context))

    signup_data = json.loads(event['body'])

    try:
        store_in_dynamo(signup_data)
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("already existing email")
            return _response(409, "Already existing")
    except Exception as ex:
        print(ex)
        return _response(500, "KO from DDB")

    try:
        publish_to_sns(signup_data)
    except Exception:
        print(ex)
        return _response(500, "KO from SNS")

    # all good
    return _response(201, "OK")

def _response(status, message):
    return {
        "body": json.dumps({"message": message}),
        "statusCode": status,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Credentials" : True,
            "Access-Control-Allow-Headers": "'x-requested-with'"
        },
    }


def store_in_dynamo(signup_data):
    DDB_TABLE.put_item(
        Item=signup_data,
        ConditionExpression="attribute_not_exists(email)",
    )


def publish_to_sns(signup_data):
    SNS.publish(
        TopicArn=SNS_TOPIC,
        Message=json.dumps(signup_data),
        Subject="New signup: %s" % signup_data['email'],
    )