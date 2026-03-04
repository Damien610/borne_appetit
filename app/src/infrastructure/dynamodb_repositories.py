import boto3
from typing import Optional
from domain.entities import Restaurant, Terminal
from domain.repositories import RestaurantRepository, TerminalRepository

class DynamoDBRestaurantRepository(RestaurantRepository):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def get_by_uuid(self, uuid: str) -> Optional[Restaurant]:
        response = self.table.get_item(Key={'PK': f'RESTAURANT#{uuid}', 'SK': 'CONFIG'})
        if 'Item' not in response:
            return None
        item = response['Item']
        return Restaurant(
            uuid=uuid,
            name=item.get('name'),
            uri_name=item.get('uri_name'),
            logo=item.get('logo'),
            primary_color=item.get('primary_color'),
            secondary_color=item.get('secondary_color')
        )
    
    def get_by_uri(self, uri: str) -> Optional[Restaurant]:
        response = self.table.query(
            IndexName='uri_name-index',
            KeyConditionExpression='uri_name = :uri',
            ExpressionAttributeValues={':uri': uri}
        )
        if not response.get('Items'):
            return None
        item = response['Items'][0]
        uuid = item['PK'].replace('RESTAURANT#', '')
        return Restaurant(
            uuid=uuid,
            name=item.get('name'),
            uri_name=item.get('uri_name'),
            logo=item.get('logo'),
            primary_color=item.get('primary_color'),
            secondary_color=item.get('secondary_color')
        )

class DynamoDBTerminalRepository(TerminalRepository):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def get_by_uuid(self, uuid: str) -> Optional[Terminal]:
        response = self.table.query(
            IndexName='SK-index',
            KeyConditionExpression='SK = :sk',
            ExpressionAttributeValues={':sk': f'TERMINAL#{uuid}'}
        )
        if not response.get('Items'):
            return None
        item = response['Items'][0]
        restaurant_uuid = item['PK'].replace('RESTAURANT#', '')
        return Terminal(
            uuid=uuid,
            restaurant_uuid=restaurant_uuid,
            name=item.get('name'),
            location=item.get('location')
        )
