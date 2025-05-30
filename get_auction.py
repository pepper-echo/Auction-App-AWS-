import json
import boto3

dynamodb = boto3.resource('dynamodb')
auctions_table = dynamodb.Table('HW09-Auctions')

def auction_handler(event, context):
    path_params = event.get('pathParameters') or {}
    auction_id = path_params.get('auctionId')
    if auction_id:
        response = auctions_table.get_item(Key={'auctionId': auction_id})
        item = response.get('Item')
        if item: # single auction
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps(item, default=str)
            }
        else: # auction not found
            return {'statusCode': 404, 'body': json.dumps({'error': 'Auction not found'})}
    else: # all auctions
        scan = auctions_table.scan()
        return {
            'statusCode': 200, 
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(scan.get('Items', []), default=str)
        }
