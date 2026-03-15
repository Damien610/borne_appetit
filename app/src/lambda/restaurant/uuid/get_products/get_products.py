import json
from infrastructure.dynamodb_products_repository import DynamoDBProductsRepository


def lambda_handler(event, context):
    restaurant_uuid = event['pathParameters']['restaurant_uuid']

    repo = DynamoDBProductsRepository()
    data = repo.get_by_restaurant(restaurant_uuid)

    result = {
        'categories': [
            {
                'uuid': c.uuid,
                'name': c.name,
                'iconUrl': c.icon_url,
                'description': c.description
            }
            for c in data['categories']
        ],
        'items': [
            {
                'uuid': p.uuid,
                'name': p.name,
                'imageUrl': p.image_url,
                'allergens': p.allergens,
                'nutritionalValues': p.nutritional_values,
                'price': p.price,
                'categories': p.categories,
                'description': p.description
            }
            for p in data['products']
        ]
    }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(result)
    }
