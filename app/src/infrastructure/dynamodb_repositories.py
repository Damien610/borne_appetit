import boto3
from typing import Optional
from domain.entities import Restaurant, Terminal
from domain.customer import Customer
from domain.repositories import RestaurantRepository, TerminalRepository, CustomerRepository

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
            favicon=item.get('favicon'),
            welcome_image=item.get('welcome_image'),
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
            favicon=item.get('favicon'),
            welcome_image=item.get('welcome_image'),
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

class DynamoDBCustomerRepository(CustomerRepository):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def get_by_loyalty_code(self, loyalty_code: str, restaurant_id: str = None) -> Optional[Customer]:
        response = self.table.query(
            IndexName='LoyaltyCodeIndex',
            KeyConditionExpression='loyalty_code = :code',
            ExpressionAttributeValues={':code': loyalty_code}
        )
        if not response.get('Items'):
            return None
        
        for item in response['Items']:
            customer_restaurant_id = item['PK'].replace('RESTAURANT#', '')
            if not restaurant_id or customer_restaurant_id == restaurant_id:
                return Customer(
                    restaurant_id=customer_restaurant_id,
                    customer_id=item['SK'].replace('CLIENT#', ''),
                    email=item['email'],
                    loyalty_code=item['loyalty_code'],
                    name=item.get('name'),
                    loyalty_points=int(item.get('loyalty_points', 0))
                )
        return None
    
    def get_by_email(self, restaurant_id: str, email: str) -> Optional[Customer]:
        pass
    
    def create(self, customer: Customer) -> Customer:
        pass
    
    def update(self, customer: Customer) -> Customer:
        pass
