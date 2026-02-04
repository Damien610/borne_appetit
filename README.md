# Borne Appetit - Infrastructure

Infrastructure as Code avec Terraform pour l'application Borne Appetit.

## 🏗️ Architecture

- **S3** : Stockage des assets statiques et images
- **CloudFront** : CDN pour la distribution du contenu
- **DynamoDB** : Base de données NoSQL (PK/SK pattern)
- **Lambda** : Fonctions serverless Python
- **API Gateway** : API REST HTTP

## 🚀 Déploiement automatique

Le déploiement se fait automatiquement via GitHub Actions à chaque push sur `main`.

### Configuration requise

1. **Créer les secrets GitHub** :
   - Aller dans `Settings` → `Secrets and variables` → `Actions`
   - Ajouter :
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`

2. **Créer un utilisateur IAM AWS** avec les permissions :
   - S3
   - CloudFront
   - DynamoDB
   - Lambda
   - API Gateway
   - IAM (pour créer les rôles)

## 📦 Déploiement manuel

```bash
cd app/tf
terraform init
terraform plan
terraform validate
terraform apply
```

## 🔒 Sécurité

- La table DynamoDB est protégée contre la suppression (`prevent_destroy`)
- Le bucket S3 est privé (accès uniquement via CloudFront)
- HTTPS obligatoire sur CloudFront

## 📁 Structure

```
app/
├── src/lambda/          # Code Python Lambda
└── tf/                  # Infrastructure Terraform
    ├── terraform.tf     # Configuration Terraform
    ├── variables.tf     # Variables
    ├── s3.tf           # Bucket S3
    ├── cloudfront.tf   # Distribution CDN
    ├── dynamodb.tf     # Table DynamoDB
    ├── lambda.tf       # Fonctions Lambda
    ├── api_gateway.tf  # API Gateway
    ├── iam.tf          # Rôles IAM
    └── outputs.tf      # Outputs
```

## 🌐 URLs après déploiement

Les URLs seront affichées après le déploiement :
- `api_gateway_url` : URL de l'API
- `cloudfront_domain_name` : URL du CDN
- `s3_bucket_name` : Nom du bucket S3
- `dynamodb_table_name` : Nom de la table DynamoDB
