import json
import os
from infrastructure.dynamodb_repositories import DynamoDBCustomerRepository
from application.use_cases import GetCustomerByLoyaltyCodeUseCase

def handler(event, context):
    restaurant_uuid = event['pathParameters']['restaurant_uuid']
    loyalty_code = event.get('queryStringParameters', {}).get('loyaltyCode') if event.get('queryStringParameters') else None

    if not loyalty_code:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'loyaltyCode required'})
        }

    table_name = os.environ['CUSTOMERS_TABLE_NAME']
    customer_repo = DynamoDBCustomerRepository(table_name)
    use_case = GetCustomerByLoyaltyCodeUseCase(customer_repo, None)

    result = use_case.execute(restaurant_uuid, loyalty_code)

    if not result:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Customer not found'})
        }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(result)
    }
