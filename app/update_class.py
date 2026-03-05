#!/usr/bin/env python3
"""Mettre à jour la classe sans reviewStatus"""

import os
import sys
import json
import requests
sys.path.insert(0, 'src')

from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Ces variables doivent être définies dans l'environnement ou via AWS Secrets Manager
# os.environ['GOOGLE_WALLET_ISSUER_ID'] = 'YOUR_ISSUER_ID'
# os.environ['GOOGLE_WALLET_SERVICE_ACCOUNT'] = 'YOUR_SERVICE_ACCOUNT_JSON'

if 'GOOGLE_WALLET_ISSUER_ID' not in os.environ or 'GOOGLE_WALLET_SERVICE_ACCOUNT' not in os.environ:
    raise ValueError("Les variables d'environnement GOOGLE_WALLET_ISSUER_ID et GOOGLE_WALLET_SERVICE_ACCOUNT doivent être définies")

issuer_id = os.environ['GOOGLE_WALLET_ISSUER_ID']
service_account_json = json.loads(os.environ['GOOGLE_WALLET_SERVICE_ACCOUNT'])

credentials = service_account.Credentials.from_service_account_info(
    service_account_json,
    scopes=['https://www.googleapis.com/auth/wallet_object.issuer']
)
credentials.refresh(Request())

class_id = f"{issuer_id}.shake-shack_loyalty"

# Mettre à jour la classe
loyalty_class = {
    "id": class_id,
    "issuerName": "Shake Shack",
    "programName": "Carte de fidélité Shake Shack",
    "programLogo": {
        "sourceUri": {
            "uri": "https://borne-appetit-assets.s3.eu-west-1.amazonaws.com/shake-shack/images/favicon.ico"
        }
    },
    "hexBackgroundColor": "#1a73e8"
}

print("📝 Mise à jour de la classe...")
response = requests.put(
    f"https://walletobjects.googleapis.com/walletobjects/v1/loyaltyClass/{class_id}",
    headers={"Authorization": f"Bearer {credentials.token}"},
    json=loyalty_class
)

if response.status_code == 200:
    print("✅ Classe mise à jour")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"❌ Erreur: {response.status_code}")
    print(response.text)
