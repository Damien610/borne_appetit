import boto3
import os
from typing import List
from domain.product import Category, Product


class DynamoDBProductsRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.environ.get('PRODUCTS_TABLE_NAME'))

    def get_by_restaurant(self, restaurant_uuid: str) -> dict:
        items = []
        params = {
            'KeyConditionExpression': 'PK = :pk',
            'ExpressionAttributeValues': {':pk': f'RESTAURANT#{restaurant_uuid}'}
        }
        while True:
            response = self.table.query(**params)
            items.extend(response['Items'])
            if 'LastEvaluatedKey' not in response:
                break
            params['ExclusiveStartKey'] = response['LastEvaluatedKey']

        categories = []
        products = []
        for item in items:
            sk = item['SK']
            if sk.startswith('CATEGORY#'):
                categories.append(Category(
                    uuid=item['uuid'],
                    name=item['name'],
                    icon_url=item.get('iconUrl', ''),
                    description=item.get('description', '')
                ))
            elif sk.startswith('ITEM#'):
                products.append(Product(
                    uuid=item['uuid'],
                    name=item['name'],
                    image_url=item.get('imageUrl', ''),
                    price=float(item.get('price', 0)),
                    description=item.get('description', ''),
                    categories=item.get('categories', []),
                    allergens=item.get('allergens', ''),
                    nutritional_values=item.get('nutritionalValues', '')
                ))

        return {'categories': categories, 'products': products}
