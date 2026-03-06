# Borne Appetit - Infrastructure

Infrastructure as Code avec Terraform pour l'application Borne Appetit.

## 🏗️ Architecture

- **S3** : Stockage des assets statiques et images
- **CloudFront** : CDN pour la distribution du contenu
- **DynamoDB** : Base de données NoSQL (PK/SK pattern)
- **Lambda** : Fonctions serverless Python avec Lambda Layers
- **API Gateway** : API REST HTTP

## 🚀 Déploiement automatique

Le déploiement se fait automatiquement via GitHub Actions à chaque push sur `main`.

### Prérequis

1. **Docker Desktop** (pour rebuild la Lambda Layer)
   - Télécharger : https://www.docker.com/products/docker-desktop/
   - Nécessaire pour compiler les dépendances Python pour Linux (AWS Lambda)
   - L'image Lambda Python (~150MB) est téléchargée automatiquement au premier build

2. **Terraform** (>= 1.0)

3. **AWS CLI** configuré avec les credentials

### Configuration requise (GitHub Actions)

1. **Créer les secrets GitHub** :
   - Aller dans `Settings` → `Secrets and variables` → `Actions`
   - Ajouter :
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`

2. **Créer un utilisateur IAM AWS** avec les permissions :
   - S3, CloudFront, DynamoDB, Lambda, API Gateway, IAM

## 📦 Déploiement manuel

```bash
cd app/tf
terraform init
terraform plan
terraform apply
```

**Note** : Terraform rebuild automatiquement la Lambda Layer si les fichiers partagés (`infrastructure/`, `application/`, `domain/`) sont modifiés.

## 🔧 Lambda Layer

La Lambda Layer contient :
- Modules Python partagés : `infrastructure/`, `application/`, `domain/`
- Dépendances pip : PyJWT, requests, google-auth, google-auth-oauthlib, boto3

### Rebuild automatique

Terraform détecte les changements et rebuild automatiquement avec Docker :

```bash
# Modifier un fichier partagé
vim app/src/infrastructure/dynamodb_repositories.py

# Terraform rebuild la layer automatiquement
cd app/tf && terraform apply
```

### Rebuild manuel (si nécessaire)

```bash
./app/build_shared_layer.sh
```

**Sans Docker** : Le script utilise la layer pré-buildée commitée dans Git (fallback automatique).

## 🔒 Sécurité

- La table DynamoDB est protégée contre la suppression (`prevent_destroy`)
- Le bucket S3 est privé (accès uniquement via CloudFront)
- HTTPS obligatoire sur CloudFront
- JWT authentication pour les routes protégées

## 📁 Structure

```
app/
├── src/
│   ├── infrastructure/      # Repositories DynamoDB
│   ├── application/         # Use cases
│   ├── domain/             # Entities
│   └── lambda/             # Lambda handlers
│       ├── health/
│       ├── terminal/
│       ├── restaurant/
│       ├── wallet/
│       └── shared_layer.zip  # Layer pré-buildée (27MB)
├── tf/                     # Infrastructure Terraform
│   ├── terraform.tf
│   ├── variables.tf
│   ├── modules/
│   │   ├── lambda/
│   │   ├── api/
│   │   └── ...
│   └── outputs.tf
└── build_shared_layer.sh   # Script de build de la layer
```

## 🌐 API Routes

Après déploiement, l'API est disponible sur `{api_gateway_url}` :

- `GET /health` - Health check
- `GET /terminal/config/{terminal_uuid}` - Configuration du terminal
- `POST /terminal/refresh-token` - Génération JWT (24h)
- `GET /restaurant/{uri}/config` - Configuration restaurant
- `GET /restaurant/{uuid}/customer?loyaltyCode={code}` - Lookup client
- `GET /restaurant/{uuid}/products` - Liste des produits
- `POST /send-loyalty-card` - Envoi carte de fidélité par email
- `POST /wallet/class/{restaurant_uuid}` - Création classe Google Wallet
- `PATCH /customer/{customer_id}/points` - Mise à jour points (JWT requis)

## 🎯 URLs après déploiement

Les URLs sont affichées après `terraform apply` :
- `api_gateway_url` : URL de l'API
- `cloudfront_domain_name` : URL du CDN
- `s3_bucket_name` : Nom du bucket S3
- `dynamodb_table_name` : Nom de la table DynamoDB
