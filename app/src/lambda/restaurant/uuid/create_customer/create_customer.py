import json
import os
import uuid
import secrets
import logging
import boto3
import requests
from infrastructure.dynamodb_repositories import DynamoDBCustomerRepository
from application.use_cases import GetCustomerByLoyaltyCodeUseCase
from domain.customer import Customer
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)
client = boto3.client('lambda')

def generate_loyalty_code() -> str:
    return ''.join(str(secrets.randbelow(10)) for _ in range(8))

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

def handler(event, context):
    try:
        restaurant_id = event['pathParameters']['restaurant_uuid']

        body = json.loads(event.get('body', ''))
        name = body.get('name', '')
        email = body.get('email', '')

        if name == '':
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'name required'})
        }

        if email == '':
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'email required'})
        }

        table_name = os.environ['CUSTOMERS_TABLE_NAME']
        customer_repo = DynamoDBCustomerRepository()
        customer_id = str(uuid.uuid4())
        loyalty_code = generate_loyalty_code()
        customer = Customer(restaurant_id=restaurant_id, customer_id=customer_id, email=email, loyalty_code=loyalty_code, name=name)
        logger.info(f"Objet client: {customer}")
        logger.info(f"table_name: {table_name}")

        # Création du client
        created_customer = customer_repo.create(customer)
        logger.info(f"Client créé: {created_customer}")

        # response_lambda = client.invoke(
        #     FunctionName='borne-appetit-send-loyalty-card',
        #     InvocationType='RequestResponse', # 'Event' pour asynchrone, 'RequestResponse' pour synchrone
        #     Payload=json.dumps({"body":{'email': created_customer.email,"restaurant_uuid":restaurant_id}})
        # )

        response_lambda = requests.post(
            'https://ubvobffhy8.execute-api.eu-west-1.amazonaws.com/send-loyalty-card',
            json={
                'email': created_customer.email,
                'restaurant_uuid': restaurant_id
            }
        )
        return response(201, {response_lambda.status_code})
    
    except ClientError as e:
            # erreur DynamoDB
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return response(409, {"message": "Le client existe déjà"})

            return response(500, {"message": "Erreur base de données"})

    except json.JSONDecodeError:
        return response(400, {"message": "JSON invalide"})

    except Exception as e:
        print("Erreur inattendue:", str(e))
        return response(500, {"message": "Erreur interne"})