import json
import jwt
import os
from application.send_loyalty_card_use_case import SendLoyaltyCardUseCase
from infrastructure.smtp_email_service import SMTPEmailService
from infrastructure.dynamodb_customer_repository import DynamoDBCustomerRepository
from infrastructure.dynamodb_repositories import DynamoDBRestaurantRepository
from infrastructure.google_wallet_service import GoogleWalletPassService


def lambda_handler(event, context):
    """Handler Lambda pour envoyer la carte de fidélité"""
    
    try:
        # Récupérer le token JWT depuis les headers
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Token manquant'})
            }
        
        token = auth_header.replace('Bearer ', '')
        
        # Décoder et vérifier le JWT
        jwt_secret = os.environ.get('JWT_SECRET')
        if not jwt_secret:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Configuration JWT manquante'})
            }
        
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            restaurant_id = payload.get('restaurant_id')
        except jwt.ExpiredSignatureError:
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Token expiré'})
            }
        except jwt.InvalidTokenError:
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Token invalide'})
            }
        
        if not restaurant_id:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Restaurant ID manquant dans le token'})
            }
        
        # Récupérer l'email depuis le body
        body = json.loads(event.get('body', '{}'))
        recipient_email = body.get('email')
        
        if not recipient_email:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Email requis'})
            }
        
        # Injection de dépendances
        config_table = os.environ.get('CONFIG_TABLE_NAME')
        customers_table = os.environ.get('CUSTOMERS_TABLE_NAME')
        
        email_service = SMTPEmailService()
        customer_repository = DynamoDBCustomerRepository(customers_table)
        restaurant_repository = DynamoDBRestaurantRepository(config_table)
        wallet_service = GoogleWalletPassService()
        
        use_case = SendLoyaltyCardUseCase(
            email_service,
            customer_repository,
            restaurant_repository,
            wallet_service
        )
        
        # Exécution
        result = use_case.execute(restaurant_id, recipient_email)
        
        if result['success']:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Email envoyé avec succès',
                    'customer_id': result['customer_id'],
                    'loyalty_code': result['loyalty_code'],
                    'wallet_url': result['wallet_url']
                })
            }
        else:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Échec envoi email'})
            }
        
    except ValueError as e:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
