import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
auctions_table = dynamodb.Table('HW09-Auctions')
users_table = dynamodb.Table('HW09-Users')
bids_table = dynamodb.Table('HW09-Bids')

def auction_handler(event, context):
    try:
        body = json.loads(event['body']) if 'body' in event else event
        auction_id = body.get('auctionId')
        
        if not auction_id:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing auctionId'})
            }

        # Get all bids for the auction
        response = bids_table.query(
            IndexName='auctionId-index',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('auctionId').eq(auction_id)
        )
        bids = response.get('Items', [])
        if not bids:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'No bids for this auction'})
            }

        # Find highest bid
        highest_bid = max(bids, key=lambda b: Decimal(str(b['bidAmt'])))
        winning_user_id = highest_bid['userId']
        bid_amt = Decimal(str(highest_bid['bidAmt']))

        # Deduct bid amount from user's accBalance
        users_table.update_item(
            Key={'userId': winning_user_id},
            UpdateExpression='SET acctBalance = acctBalance - :b',
            ExpressionAttributeValues={':b': bid_amt}
        )

        # Mark auction as closed and update winningUserId
        auctions_table.update_item(
            Key={'auctionId': auction_id},
            UpdateExpression='SET #s = :s, winningUserId = :w',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':s': 'closed', ':w': winning_user_id}
        )

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Auction closed',
                'winner': winning_user_id,
                'amount': str(bid_amt)
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
