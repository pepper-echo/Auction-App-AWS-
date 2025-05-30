import json
import boto3

dynamodb = boto3.resource('dynamodb')
auctions_table = dynamodb.Table('HW09-Auctions')

def validation_handler(event, context):
    auction_id = event['auctionId']
    response = auctions_table.get_item(Key={'auctionId': auction_id})
    if 'Item' not in response:
        raise Exception(f"Auction {auction_id} does not exist")
    event['auction'] = response['Item']
    return event
