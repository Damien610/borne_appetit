import json
import os
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from infrastructure.dynamodb_repositories import DynamoDBRestaurantRepository


def lambda_handler(event, context):
    """Handler Lambda pour créer/mettre à jour une classe Google Wallet pour un restaurant"""
    
    try:
        # Récupérer le restaurant_id depuis le path
        restaurant_id = event.get('pathParameters', {}).get('restaurant_id')
        
        if not restaurant_id:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Restaurant ID requis'})
            }
        
        # Récupérer la config du restaurant
        config_table = os.environ.get('CONFIG_TABLE_NAME')
        restaurant_repo = DynamoDBRestaurantRepository(config_table)
        restaurant = restaurant_repo.get_by_uuid(restaurant_id)
        
        if not restaurant:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Restaurant introuvable'})
            }
        
        # Credentials Google Wallet
        issuer_id = os.environ.get('GOOGLE_WALLET_ISSUER_ID')
        service_account_json = json.loads(os.environ.get('GOOGLE_WALLET_SERVICE_ACCOUNT'))
        
        credentials = service_account.Credentials.from_service_account_info(
            service_account_json,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer']
        )
        credentials.refresh(Request())
        
        # Créer la classe
        class_id = f"{issuer_id}.{restaurant.uri_name}_loyalty_v2"
        
        # Conversion couleur oklch -> hex (simplifié)
        hex_color = "#1a73e8"
        if restaurant.primary_color and '136.559' in restaurant.primary_color:
            hex_color = "#5cb85c"
        
        loyalty_class = {
            "id": class_id,
            "issuerName": restaurant.name,
            "programName": f"Carte de fidélité {restaurant.name}",
            "programLogo": {
                "sourceUri": {
                    "uri": restaurant.favicon
                }
            },
            "hexBackgroundColor": hex_color,
            "reviewStatus": "UNDER_REVIEW"
        }
        
        # Essayer de créer la classe
        response = requests.post(
            "https://walletobjects.googleapis.com/walletobjects/v1/loyaltyClass",
            headers={"Authorization": f"Bearer {credentials.token}"},
            json=loyalty_class
        )
        
        if response.status_code == 200:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Classe créée avec succès',
                    'class_id': class_id
                })
            }
        elif response.status_code == 409:
            # Classe existe déjà, la mettre à jour
            response = requests.put(
                f"https://walletobjects.googleapis.com/walletobjects/v1/loyaltyClass/{class_id}",
                headers={"Authorization": f"Bearer {credentials.token}"},
                json=loyalty_class
            )
            
            if response.status_code == 200:
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'message': 'Classe mise à jour avec succès',
                        'class_id': class_id
                    })
                }
            else:
                return {
                    'statusCode': response.status_code,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'error': 'Erreur mise à jour classe',
                        'details': response.text
                    })
                }
        else:
            return {
                'statusCode': response.status_code,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Erreur création classe',
                    'details': response.text
                })
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
