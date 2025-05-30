import json
import boto3
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
bids_table = dynamodb.Table('HW09-Bids')

def store_handler(event, context):
    timestamp = datetime.now(timezone.utc).isoformat()

    bid_item = {
        'auctionId': event['auctionId'],
        'userId': event['userId'],
        'bidAmt': event['bidAmt'],
        'date': timestamp
    }

    # Store the bid item in the DynamoDB table
    bids_table.put_item(Item=bid_item)
    event['newBid'] = bid_item
    return event