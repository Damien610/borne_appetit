import json
import os
import jwt
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from infrastructure.dynamodb_customer_repository import DynamoDBCustomerRepository


def lambda_handler(event, context):
    """Handler Lambda pour mettre à jour les points de fidélité d'un client"""
    
    try:
        # Vérifier le token JWT
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Token manquant'})
            }
        
        token = auth_header.replace('Bearer ', '')
        jwt_secret = os.environ.get('JWT_SECRET')
        
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            restaurant_id = payload.get('restaurant_id')
        except:
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Token invalide'})
            }
        
        # Récupérer customer_id et nouveaux points
        customer_id = event.get('pathParameters', {}).get('customer_id')
        body = json.loads(event.get('body', '{}'))
        new_points = body.get('points')
        
        if not customer_id or new_points is None:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'customer_id et points requis'})
            }
        
        # Récupérer le client depuis DynamoDB
        customers_table = os.environ.get('CUSTOMERS_TABLE_NAME')
        customer_repo = DynamoDBCustomerRepository(customers_table)
        
        # Mettre à jour les points dans DynamoDB
        # TODO: Implémenter customer_repo.update_points(customer_id, new_points)
        
        # Mettre à jour l'objet Google Wallet
        issuer_id = os.environ.get('GOOGLE_WALLET_ISSUER_ID')
        service_account_json = json.loads(os.environ.get('GOOGLE_WALLET_SERVICE_ACCOUNT'))
        
        credentials = service_account.Credentials.from_service_account_info(
            service_account_json,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer']
        )
        credentials.refresh(Request())
        
        object_id = f"{issuer_id}.{customer_id}"
        
        # Récupérer l'objet actuel
        response = requests.get(
            f"https://walletobjects.googleapis.com/walletobjects/v1/loyaltyObject/{object_id}",
            headers={"Authorization": f"Bearer {credentials.token}"}
        )
        
        if response.status_code != 200:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Objet Wallet introuvable'})
            }
        
        wallet_object = response.json()
        
        # Mettre à jour les points
        wallet_object['loyaltyPoints']['balance']['int'] = new_points
        
        # Envoyer la mise à jour
        response = requests.put(
            f"https://walletobjects.googleapis.com/walletobjects/v1/loyaltyObject/{object_id}",
            headers={"Authorization": f"Bearer {credentials.token}"},
            json=wallet_object
        )
        
        if response.status_code == 200:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Points mis à jour avec succès',
                    'customer_id': customer_id,
                    'points': new_points
                })
            }
        else:
            return {
                'statusCode': response.status_code,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Erreur mise à jour Wallet',
                    'details': response.text
                })
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
