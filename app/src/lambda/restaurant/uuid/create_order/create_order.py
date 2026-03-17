import json
import os
import uuid
import random
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ORDER_TABLE_NAME'])


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))

        restaurant_uuid = event['pathParameters']['restaurant_uuid']
        items = body.get('items')
        service_mode = body.get('serviceMode')
        total_price = body.get('totalPrice')

        if not items or not service_mode or total_price is None:
            return response(400, {"error": "items, serviceMode and totalPrice are required"})

        order_number = random.randint(1, 99)
        order_id = str(uuid.uuid4())

        item = {
            'PK': f"RESTAURANT#{restaurant_uuid}",
            'SK': f"ORDER#{order_id}",
            'orderNumber': order_number,
            'serviceMode': service_mode,
            'totalPrice': Decimal(str(total_price)),
            'items': json.dumps(items),
        }

        customer_uuid = body.get('customerUuid')
        if customer_uuid:
            item['customerUuid'] = customer_uuid

        easel_code = body.get('easelCode')
        if easel_code:
            item['easelCode'] = easel_code

        table.put_item(Item=item)

        return response(201, {"orderNumber": order_number})

    except json.JSONDecodeError:
        return response(400, {"error": "Invalid JSON"})
    except Exception as e:
        print("Error:", str(e))
        return response(500, {"error": "Internal server error"})
