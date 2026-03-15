import boto3
import os
import uuid
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
            secondary_color=item.get('secondary_color'),
            primary_hexa=item.get('primary_hexa'),
            secondary_hexa=item.get('secondary_hexa')
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
            secondary_color=item.get('secondary_color'),
            primary_hexa=item.get('primary_hexa'),
            secondary_hexa=item.get('secondary_hexa')
        )

class DynamoDBTerminalRepository(TerminalRepository):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def get_by_uuid(self, uuid: str) -> Optional[Terminal]:
        # Scan pour trouver le terminal (moins performant mais fonctionne)
        response = self.table.scan(
            FilterExpression='SK = :sk',
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
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.environ.get('CUSTOMERS_TABLE_NAME'))
    
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
        response = self.table.query(
            IndexName='RestaurantEmailIndex',
            KeyConditionExpression='restaurant_email = :re',
            ExpressionAttributeValues={
                ':re': f"{restaurant_id}#{email}"
            }
        )
        items = response.get('Items', [])
        if not items:
            return None
        item = items[0]
        return Customer(
            restaurant_id=item['PK'].replace('RESTAURANT#', ''),
            customer_id=item['SK'].replace('CLIENT#', ''),
            email=item['email'],
            loyalty_code=item['loyalty_code'],
            name=item.get('name'),
            loyalty_points=int(item.get('loyalty_points', 0))
        )
    
    def create(self, customer: Customer) -> Customer:
        """Crée un nouveau client"""       
        item = {
            'PK': f"RESTAURANT#{customer.restaurant_id}",
            'SK': f"CLIENT#{customer.customer_id}",
            'name': customer.name,
            'email': customer.email,
            'loyalty_code': customer.loyalty_code,
            'loyalty_points': customer.loyalty_points,
            'restaurant_email': f"{customer.restaurant_id}#{customer.email}"
        }
        
        self.table.put_item(
                Item=item,
                ConditionExpression='attribute_not_exists(PK) AND attribute_not_exists(SK)'
            )
        return customer
    
    def update(self, customer: Customer) -> Customer:
        pass
