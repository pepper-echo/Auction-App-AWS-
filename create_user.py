import json
import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('HW09-Users')

def user_handler(event, context):
    try:
        body = json.loads(event['body']) if 'body' in event else event
        users_table.put_item(Item=body)
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'User created', 'user': body}, default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
