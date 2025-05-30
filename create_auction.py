import json
import boto3

dynamodb = boto3.resource('dynamodb')
auctions_table = dynamodb.Table('HW09-Auctions')

def auction_handler(event, context):
    try:
        body = json.loads(event['body']) if 'body' in event else event
        auctions_table.put_item(Item=body)
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Auction created', 'auction': body}, default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
