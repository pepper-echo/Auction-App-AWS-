import json
import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('HW09-Users')

def user_handler(event, context):
    path_params = event.get('pathParameters') or {}
    user_id = path_params.get('userId')
    
    if user_id:
        response = users_table.get_item(Key={'userId': user_id})
        item = response.get('Item')
        if item: # single user
            return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(item, default=str) 
        }
        else: # user not found
            return {'statusCode': 404, 'body': json.dumps({'error': 'User not found'})}
    else:   # all users
        scan = users_table.scan()
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(scan.get('Items', []), default=str)
        }
