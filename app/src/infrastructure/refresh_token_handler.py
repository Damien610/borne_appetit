import json
import jwt
import os
from datetime import datetime, timedelta
from infrastructure.dynamodb_repositories import DynamoDBTerminalRepository


def lambda_handler(event, context):
    """Handler Lambda pour générer un token JWT pour un terminal"""
    
    try:
        body = json.loads(event.get('body', '{}'))
        terminal_uuid = body.get('terminal_uuid')
        
        if not terminal_uuid:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Terminal UUID requis'})
            }
        
        # Vérifier que le terminal existe
        table_name = os.environ.get('CONFIG_TABLE_NAME')
        terminal_repo = DynamoDBTerminalRepository(table_name)
        terminal = terminal_repo.get_by_uuid(terminal_uuid)
        
        if not terminal:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Terminal non trouvé'})
            }
        
        # Générer le JWT valide 24h
        jwt_secret = os.environ.get('JWT_SECRET')
        if not jwt_secret:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Configuration JWT manquante'})
            }
        
        payload = {
            'restaurant_id': terminal.restaurant_uuid,
            'terminal_id': terminal_uuid,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        
        token = jwt.encode(payload, jwt_secret, algorithm='HS256')
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'token': token,
                'expires_in': 86400  # 24h en secondes
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
