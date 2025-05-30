import json
import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('HW09-Users')

def validation_handler(event, context):
    user_id = event['userId']
    response = users_table.get_item(Key={'userId': user_id})
    if 'Item' not in response:
        raise Exception(f"User {user_id} does not exist")
    event['user'] = response['Item']
    return event
