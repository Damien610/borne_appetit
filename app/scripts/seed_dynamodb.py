#!/usr/bin/env python3
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('borne-appetit-config')

# Suppression des anciennes données
scan = table.scan()
with table.batch_writer() as batch:
    for item in scan['Items']:
        batch.delete_item(Key={'PK': item['PK'], 'SK': item['SK']})

print("✓ Table vidée")

restaurant_uuid = '2f973077-158e-4337-8507-ff348e99bf03'

# Restaurant
table.put_item(Item={
    'PK': f'RESTAURANT#{restaurant_uuid}',
    'SK': 'CONFIG',
    'name': 'Shake Shack',
    'uri_name': 'shake-shack',
    'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Shake_Shack_logo.svg/2560px-Shake_Shack_logo.svg.png',
    'primary_color': 'oklch(0.553 0.158 136.559)',
    'secondary_color': 'oklch(0.984 0.003 247.858)'
})

# Terminaux
table.put_item(Item={
    'PK': f'RESTAURANT#{restaurant_uuid}',
    'SK': 'TERMINAL#cebbe9f9-637b-4220-aad4-7ab299c007f1',
    'name': 'Borne 001'
})

table.put_item(Item={
    'PK': f'RESTAURANT#{restaurant_uuid}',
    'SK': 'TERMINAL#57ec4e4c-533a-4854-98cd-c00360805eed',
    'name': 'Borne 002'
})

print("✓ Données insérées")
