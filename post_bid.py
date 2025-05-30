import json
import boto3
import os

step_client = boto3.client('stepfunctions')

def bids_handler(event, context):
    state_machine_arn = os.environ['STEP_FUNCTION_ARN']
    body = json.loads(event['body'])  
    response = step_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(body)  
    )
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Bid submission started', 'executionArn': response['executionArn']})
    }
