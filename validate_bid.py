import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
bids_table = dynamodb.Table('HW09-Bids')

def validation_handler(event, context):
    user = event['user']
    auction = event['auction']
    bid_amt = Decimal(str(event['bidAmt']))

    # Check reserve price
    reserve = Decimal(str(auction.get('reserve', '0')))
    if bid_amt < reserve:
        raise Exception("Bid is below the auction's reserve price")

    # Check user balance
    if Decimal(str(user['acctBalance'])) < bid_amt:
        raise Exception("User balance is too low")

    # Check if bid is higher than existing
    response = bids_table.query(
        IndexName='auctionId-index',
        KeyConditionExpression=Key('auctionId').eq(event['auctionId'])
    )
    highest = max(
        (Decimal(str(b['bidAmt'])) for b in response.get('Items', [])),
        default=Decimal('0')
    )

    if bid_amt <= highest:
        raise Exception("Bid is not higher than current highest")

    return event
