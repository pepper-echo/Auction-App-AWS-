import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
bids_table = dynamodb.Table('HW09-Bids')

def bids_handler(event, context):
    try:
        auction_id = (event.get('queryStringParameters') or {}).get('auctionId')
        if not auction_id:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing auction query param'})
            }

        response = bids_table.query(
            IndexName='auctionId-index',
            KeyConditionExpression=Key('auctionId').eq(auction_id)
        )

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(response.get('Items', []), default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
