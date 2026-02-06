#!/usr/bin/env python3
"""
Script pour générer des données de test pour Borne Appetit
"""
import boto3
from datetime import datetime

# Configuration
REGION = 'eu-west-1'
TABLE_PRODUCTS = 'borne-appetit-table'
TABLE_CONFIG = 'borne-appetit-config'
RESTAURANT_ID = 'REST#001'

# Initialiser DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table_products = dynamodb.Table(TABLE_PRODUCTS)
table_config = dynamodb.Table(TABLE_CONFIG)

# Données produits
products = [
    {
        'PK': RESTAURANT_ID,
        'SK': 'ITEM#BURGER_001',
        'Type': 'PRODUIT',
        'nom': 'Cheeseburger Classic',
        'prix_solo': 12.50,
        'stock': 50,
        'image_url': 'https://votre-cloudfront.net/images/cheeseburger.jpg',
        'description': 'Burger avec cheddar, salade, tomate, oignons',
        'categorie': 'Burgers',
        'disponible': True
    },
    {
        'PK': RESTAURANT_ID,
        'SK': 'ITEM#BURGER_002',
        'Type': 'PRODUIT',
        'nom': 'Bacon Burger',
        'prix_solo': 14.00,
        'stock': 40,
        'image_url': 'https://votre-cloudfront.net/images/bacon-burger.jpg',
        'description': 'Burger avec bacon croustillant et cheddar',
        'categorie': 'Burgers',
        'disponible': True
    },
    {
        'PK': RESTAURANT_ID,
        'SK': 'ITEM#FRITES_001',
        'Type': 'PRODUIT',
        'nom': 'Frites Maison',
        'prix_solo': 4.50,
        'stock': 100,
        'image_url': 'https://votre-cloudfront.net/images/frites.jpg',
        'description': 'Frites fraîches coupées maison',
        'categorie': 'Accompagnements',
        'disponible': True
    },
    {
        'PK': RESTAURANT_ID,
        'SK': 'ITEM#BOISSON_001',
        'Type': 'PRODUIT',
        'nom': 'Coca-Cola 33cl',
        'prix_solo': 3.00,
        'stock': 200,
        'image_url': 'https://votre-cloudfront.net/images/coca.jpg',
        'description': 'Coca-Cola canette 33cl',
        'categorie': 'Boissons',
        'disponible': True
    },
    {
        'PK': RESTAURANT_ID,
        'SK': 'ITEM#DESSERT_001',
        'Type': 'PRODUIT',
        'nom': 'Brownie Chocolat',
        'prix_solo': 5.50,
        'stock': 30,
        'image_url': 'https://votre-cloudfront.net/images/brownie.jpg',
        'description': 'Brownie au chocolat maison',
        'categorie': 'Desserts',
        'disponible': True
    }
]

# Données menus/formules
menus = [
    {
        'PK': RESTAURANT_ID,
        'SK': 'FORMULE#MIDI_001',
        'Type': 'MENU',
        'nom': 'Menu Midi',
        'prix': 15.90,
        'description': 'Burger + Frites + Boisson',
        'items': ['ITEM#BURGER_001', 'ITEM#FRITES_001', 'ITEM#BOISSON_001'],
        'disponible': True,
        'horaires': '11:00-14:30'
    },
    {
        'PK': RESTAURANT_ID,
        'SK': 'FORMULE#MAXI_001',
        'Type': 'MENU',
        'nom': 'Menu Maxi',
        'prix': 19.90,
        'description': 'Burger + Frites + Boisson + Dessert',
        'items': ['ITEM#BURGER_002', 'ITEM#FRITES_001', 'ITEM#BOISSON_001', 'ITEM#DESSERT_001'],
        'disponible': True
    }
]

# Configuration restaurant
restaurant_config = {
    'PK': RESTAURANT_ID,
    'SK': 'CONFIG',
    'nom_restaurant': 'Borne Appetit Paris Centre',
    'adresse': '10 rue de la Paix, 75002 Paris',
    'telephone': '+33 1 42 00 00 00',
    'email': 'contact@borne-appetit.fr',
    'horaires': {
        'lundi': '11:00-22:00',
        'mardi': '11:00-22:00',
        'mercredi': '11:00-22:00',
        'jeudi': '11:00-22:00',
        'vendredi': '11:00-23:00',
        'samedi': '11:00-23:00',
        'dimanche': '12:00-22:00'
    },
    'tva': 10.0,
    'devise': 'EUR',
    'langue_defaut': 'fr'
}

# Terminaux
terminals = [
    {
        'PK': RESTAURANT_ID,
        'SK': 'TERMINAL#001',
        'terminal_id': 'TERM001',
        'nom': 'Borne Entrée Principale',
        'statut': 'actif',
        'emplacement': 'Entrée principale',
        'derniere_connexion': datetime.now().isoformat(),
        'version_logiciel': '1.0.0'
    },
    {
        'PK': RESTAURANT_ID,
        'SK': 'TERMINAL#002',
        'terminal_id': 'TERM002',
        'nom': 'Borne Salle',
        'statut': 'actif',
        'emplacement': 'Salle principale',
        'derniere_connexion': datetime.now().isoformat(),
        'version_logiciel': '1.0.0'
    },
    {
        'PK': RESTAURANT_ID,
        'SK': 'TERMINAL#003',
        'terminal_id': 'TERM003',
        'nom': 'Borne Drive',
        'statut': 'maintenance',
        'emplacement': 'Drive extérieur',
        'derniere_connexion': datetime.now().isoformat(),
        'version_logiciel': '0.9.5'
    }
]

def insert_data():
    """Insérer toutes les données dans DynamoDB"""
    
    print("🍔 Insertion des produits...")
    for product in products:
        table_products.put_item(Item=product)
        print(f"  ✅ {product['nom']}")
    
    print("\n📋 Insertion des menus...")
    for menu in menus:
        table_products.put_item(Item=menu)
        print(f"  ✅ {menu['nom']}")
    
    print("\n🏪 Insertion de la configuration restaurant...")
    table_config.put_item(Item=restaurant_config)
    print(f"  ✅ {restaurant_config['nom_restaurant']}")
    
    print("\n🖥️  Insertion des terminaux...")
    for terminal in terminals:
        table_config.put_item(Item=terminal)
        print(f"  ✅ {terminal['nom']} ({terminal['statut']})")
    
    print("\n✨ Données insérées avec succès !")
    print(f"\n📊 Résumé :")
    print(f"  - {len(products)} produits")
    print(f"  - {len(menus)} menus")
    print(f"  - 1 restaurant")
    print(f"  - {len(terminals)} terminaux")

if __name__ == '__main__':
    try:
        insert_data()
    except Exception as e:
        print(f"❌ Erreur : {e}")
