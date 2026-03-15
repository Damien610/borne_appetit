import json
import os
import uuid
import smtplib
import requests
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from infrastructure.dynamodb_repositories import DynamoDBCustomerRepository, DynamoDBRestaurantRepository
from google.oauth2 import service_account
from google.auth.transport.requests import Request


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """Envoie une carte de fidélité par email"""
    try:
        logger.info(f"debug_evenement: {event}")
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        restaurant_uuid = body.get('restaurant_uuid')

        if not email or not restaurant_uuid:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Email et restaurant_uuid requis'})
            }

        # Récupérer le restaurant
        config_table = os.environ.get('CONFIG_TABLE_NAME', 'borne-appetit-config')
        logger.info(f"[STEP 1] Recherche restaurant {restaurant_uuid} dans table {config_table}")
        restaurant_repo = DynamoDBRestaurantRepository(config_table)
        restaurant = restaurant_repo.get_by_uuid(restaurant_uuid)

        if not restaurant:
            logger.error(f"[STEP 1] Restaurant {restaurant_uuid} introuvable")
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Restaurant introuvable'})
            }
        logger.info(f"[STEP 1] Restaurant trouvé: {restaurant.name}")

        customer_repo = DynamoDBCustomerRepository()
        logger.info(f"[STEP 2] Recherche customer par email {email} pour restaurant {restaurant_uuid}")
        customer = customer_repo.get_by_email(restaurant_uuid, email)

        if not customer:
            logger.error(f"[STEP 2] Customer introuvable pour email={email}, restaurant={restaurant_uuid}")
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Client introuvable'})
            }
        logger.info(f"[STEP 2] Customer trouvé: loyalty_code={customer.loyalty_code}, points={customer.loyalty_points}")

        # Créer l'objet Google Wallet
        issuer_id = os.environ.get('GOOGLE_WALLET_ISSUER_ID')
        logger.info(f"[STEP 3] Google Wallet issuer_id={issuer_id}")
        service_account_json = json.loads(os.environ.get('GOOGLE_WALLET_SERVICE_ACCOUNT'))

        credentials = service_account.Credentials.from_service_account_info(
            service_account_json,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer']
        )
        credentials.refresh(Request())

        class_id = f"{issuer_id}.{restaurant.uri_name}_loyalty_v2"
        object_id = f"{issuer_id}.{customer.loyalty_code}"

        loyalty_object = {
            "id": object_id,
            "classId": class_id,
            "state": "ACTIVE",
            "accountId": customer.loyalty_code,
            "accountName": email,
            "loyaltyPoints": {
                "balance": {
                    "int": customer.loyalty_points or 0
                }
            },
            "barcode": {
                "type": "QR_CODE",
                "value": customer.loyalty_code
            }
        }

        # Créer ou mettre à jour l'objet via REST API
        logger.info(f"[STEP 4] POST loyaltyObject, class_id={class_id}, object_id={object_id}")
        response = requests.post(
            "https://walletobjects.googleapis.com/walletobjects/v1/loyaltyObject",
            headers={"Authorization": f"Bearer {credentials.token}"},
            json=loyalty_object
        )
        logger.info(f"[STEP 4] Wallet API response: status={response.status_code}, body={response.text[:500]}")

        if response.status_code == 409:
            # Objet existe déjà, le mettre à jour
            put_resp = requests.put(
                f"https://walletobjects.googleapis.com/walletobjects/v1/loyaltyObject/{object_id}",
                headers={"Authorization": f"Bearer {credentials.token}"},
                json=loyalty_object
            )
            logger.info(f"[STEP 4] Wallet PUT response: status={put_resp.status_code}")

        # Créer un JWT signé pour le lien "Add to Google Wallet"
        import jwt as pyjwt
        
        jwt_payload = {
            "iss": service_account_json['client_email'],
            "aud": "google",
            "typ": "savetowallet",
            "origins": [],
            "payload": {
                "loyaltyObjects": [loyalty_object]
            }
        }
        
        signed_jwt = pyjwt.encode(
            jwt_payload,
            service_account_json['private_key'],
            algorithm='RS256'
        )
        
        wallet_url = f"https://pay.google.com/gp/v/save/{signed_jwt}"

        # Envoyer l'email
        smtp_user = os.environ.get('SMTP_USER')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        logger.info(f"[STEP 5] Envoi email à {email}, smtp_user={smtp_user}, smtp_password_set={bool(smtp_password)}")

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Votre carte de fidélité {restaurant.name}"
        msg['From'] = smtp_user
        msg['To'] = email

        html = f"""
        <html>
          <body>
            <h2>Bienvenue chez {restaurant.name} !</h2>
            <p>Votre code de fidélité : <strong>{customer.loyalty_code}</strong></p>
            <p>Points actuels : {customer.loyalty_points or 0}</p>
            <p><a href="{wallet_url}">Ajouter à Google Wallet</a></p>
          </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        logger.info(f"[STEP 5] Email envoyé avec succès à {email}")

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': 'Carte de fidélité envoyée',
                'loyalty_code': customer.loyalty_code,
                'wallet_url': wallet_url
            })
        }

    except Exception as e:
        logger.error(f"[ERROR] {type(e).__name__}: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
