import os
import json
import time
from google.auth import crypt, jwt
from google.oauth2 import service_account


class GoogleWalletPassService:
    """Service pour générer des passes Google Wallet"""
    
    def __init__(self):
        self.issuer_id = os.environ.get('GOOGLE_WALLET_ISSUER_ID')
        self.service_account_json = os.environ.get('GOOGLE_WALLET_SERVICE_ACCOUNT')
        
        if not self.issuer_id:
            raise ValueError("GOOGLE_WALLET_ISSUER_ID manquant")
        
        if self.service_account_json:
            self.service_account = json.loads(self.service_account_json)
            self.credentials = service_account.Credentials.from_service_account_info(
                self.service_account,
                scopes=['https://www.googleapis.com/auth/wallet_object.issuer']
            )
        else:
            self.credentials = None
    
    def _oklch_to_hex(self, oklch_color: str) -> str:
        """Convertit oklch en hex"""
        if not oklch_color or not oklch_color.startswith('oklch'):
            return "#1a73e8"
        
        # Mapping manuel pour les couleurs connues
        # oklch(0.553 0.158 136.559) = vert Shake Shack
        if '136.559' in oklch_color:
            return "#5cb85c"  # Vert
        
        return "#1a73e8"  # Bleu par défaut
    
    def create_loyalty_pass(self, customer_id: str, loyalty_code: str, loyalty_points: int, restaurant_config: dict) -> str:
        """Crée un pass de fidélité Google Wallet avec JWT (thin JWT)"""
        
        if not self.credentials:
            raise ValueError("Credentials Google Wallet manquantes")
        
        # Ajouter un suffixe unique pour forcer la nouvelle couleur
        class_id = f"{self.issuer_id}.{restaurant_config.get('uri_name', 'default')}_loyalty_v2"
        object_id = f"{self.issuer_id}.{customer_id}"
        
        # Créer le payload avec la classe ET l'objet
        payload = {
            "iss": self.credentials.service_account_email,
            "aud": "google",
            "typ": "savetowallet",
            "iat": int(time.time()),
            "origins": ["https://borne-appetit.com"],
            "payload": {
                "loyaltyClasses": [{
                    "id": class_id,
                    "issuerName": restaurant_config.get('name', 'Restaurant'),
                    "programName": f"Carte de fidélité {restaurant_config.get('name', '')}",
                    "programLogo": {
                        "sourceUri": {
                            "uri": restaurant_config.get('favicon', '')
                        }
                    },
                    "hexBackgroundColor": self._oklch_to_hex(restaurant_config.get('primary_color', '')),
                    "reviewStatus": "UNDER_REVIEW"
                }],
                "loyaltyObjects": [{
                    "id": object_id,
                    "classId": class_id,
                    "state": "ACTIVE",
                    "accountName": loyalty_code,
                    "accountId": loyalty_code,
                    "loyaltyPoints": {
                        "balance": {"int": loyalty_points},
                        "label": "Points"
                    },
                    "barcode": {
                        "type": "QR_CODE",
                        "value": loyalty_code
                    },
                    "heroImage": {
                        "sourceUri": {
                            "uri": restaurant_config.get('welcome_image', '')
                        }
                    }
                }]
            }
        }
        
        # Signer le JWT
        token = jwt.encode(self.credentials.signer, payload)
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        return f"https://pay.google.com/gp/v/save/{token}"
