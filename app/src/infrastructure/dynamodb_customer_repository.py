import boto3
import os
import uuid
import random
import string
from typing import Optional
from datetime import datetime
from domain.customer import Customer
from domain.repositories import CustomerRepository


class DynamoDBCustomerRepository(CustomerRepository):
    """Implémentation DynamoDB du repository Customer"""
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.environ.get('CUSTOMERS_TABLE_NAME'))
    
    def get_by_email(self, restaurant_id: str, email: str) -> Optional[Customer]:
        """Récupère un client par email et restaurant"""
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
        return self._item_to_customer(item)
    
    def get_by_loyalty_code(self, loyalty_code: str) -> Optional[Customer]:
        """Récupère un client par code de fidélité"""
        response = self.table.query(
            IndexName='LoyaltyCodeIndex',
            KeyConditionExpression='loyalty_code = :lc',
            ExpressionAttributeValues={
                ':lc': loyalty_code
            }
        )
        
        items = response.get('Items', [])
        if not items:
            return None
        
        item = items[0]
        return self._item_to_customer(item)
    
    def create(self, customer: Customer) -> Customer:
        """Crée un nouveau client"""
        if not customer.customer_id:
            customer.customer_id = str(uuid.uuid4())
        
        if not customer.loyalty_code:
            customer.loyalty_code = self._generate_loyalty_code()
        
        item = {
            'PK': f"RESTAURANT#{customer.restaurant_id}",
            'SK': f"CLIENT#{customer.customer_id}",
            'name': customer.name,
            'emayil': customer.email,
            'loyalty_code': customer.loyalty_code,
            'loyalty_points': customer.loyalty_points,
            'restaurant_email': f"{customer.restaurant_id}#{customer.email}"
        }
        
        if customer.order_date:
            item['order_date'] = customer.order_date.isoformat()
        
        self.table.put_item(Item=item)
        return customer
    
    def update(self, customer: Customer) -> Customer:
        """Met à jour un client existant"""
        update_expr = "SET loyalty_points = :lp"
        expr_values = {':lp': customer.loyalty_points}
        
        if customer.order_date:
            update_expr += ", order_date = :od"
            expr_values[':od'] = customer.order_date.isoformat()
        
        self.table.update_item(
            Key={
                'PK': f"RESTAURANT#{customer.restaurant_id}",
                'SK': f"CLIENT#{customer.customer_id}"
            },
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values
        )
        
        return customer
    
    def _item_to_customer(self, item: dict) -> Customer:
        """Convertit un item DynamoDB en Customer"""
        restaurant_id = item['PK'].replace('RESTAURANT#', '')
        customer_id = item['SK'].replace('CLIENT#', '')
        
        order_date = None
        if 'order_date' in item:
            order_date = datetime.fromisoformat(item['order_date'])
        
        return Customer(
            restaurant_id=restaurant_id,
            customer_id=customer_id,
            email=item['email'],
            loyalty_code=item['loyalty_code'],
            loyalty_points=item.get('loyalty_points', 0),
            order_date=order_date
        )
    
    def _generate_loyalty_code(self) -> str:
        """Génère un code de fidélité unique (8 caractères alphanumériques)"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
