import json
import os
from infrastructure.dynamodb_repositories import DynamoDBTerminalRepository, DynamoDBRestaurantRepository
from application.use_cases import GetTerminalConfigUseCase

def handler(event, context):
    table_name = os.environ['CONFIG_TABLE_NAME']
    terminal_uuid = event['pathParameters']['uuid']
    
    terminal_repo = DynamoDBTerminalRepository(table_name)
    restaurant_repo = DynamoDBRestaurantRepository(table_name)
    use_case = GetTerminalConfigUseCase(terminal_repo, restaurant_repo)
    
    result = use_case.execute(terminal_uuid)
    
    if not result:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Terminal not found'})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
