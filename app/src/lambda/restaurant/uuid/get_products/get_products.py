import json

def lambda_handler(event, context):
    return {
        'statusCode': 400,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'TEST MAXIME'})
    }
