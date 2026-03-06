import json
import os
from infrastructure.dynamodb_repositories import DynamoDBRestaurantRepository
from application.use_cases import GetRestaurantConfigUseCase

def handler(event, context):
    table_name = os.environ['CONFIG_TABLE_NAME']
    uri = event['pathParameters']['uri']

    repository = DynamoDBRestaurantRepository(table_name)
    use_case = GetRestaurantConfigUseCase(repository)

    result = use_case.execute(uri)

    if not result:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Restaurant not found'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
