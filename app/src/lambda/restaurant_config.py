import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CONFIG_TABLE_NAME'])

def handler(event, context):
    uri = event['pathParameters']['uri']
    
    try:
        restaurant_response = table.query(
            IndexName='uri_name-index',
            KeyConditionExpression='uri_name = :uri',
            ExpressionAttributeValues={':uri': uri}
        )
        
        if not restaurant_response.get('Items'):
            return {'statusCode': 404, 'body': json.dumps({'error': 'Restaurant not found'})}
        
        restaurant = restaurant_response['Items'][0]
        restaurant_uuid = restaurant['PK'].split('#')[1]

        styles_response = table.query(
            KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
            ExpressionAttributeValues={':pk': f'RESTAURANT#{restaurant_uuid}', ':sk': 'STYLE#'}
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'restaurant': {
                    'uri_name': restaurant.get('uri_name', ''),
                    'name': restaurant.get('name', ''),
                    'logo': restaurant.get('logo', ''),
                    'favicon': restaurant.get('favicon', ''),
                    'uuid': restaurant_uuid
                },
                'styles': [{'uuid': s['SK'].split('#')[1], 'name': s.get('name', ''), 'style_value': s.get('style_value', '')} for s in styles_response.get('Items', [])]
            })
        }
    except Exception as e:
        logger.error(f'Error: {str(e)}', exc_info=True)
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
