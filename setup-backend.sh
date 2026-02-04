#!/bin/bash
set -e

REGION="eu-west-1"
BUCKET="borne-appetit-terraform-state"
TABLE="borne-appetit-terraform-locks"

echo "🚀 Configuration du backend Terraform..."

# Créer le bucket S3
echo "📦 Création du bucket S3..."
aws s3api create-bucket \
  --bucket $BUCKET \
  --region $REGION \
  --create-bucket-configuration LocationConstraint=$REGION 2>/dev/null || echo "  Bucket existe déjà"

# Activer le versioning
aws s3api put-bucket-versioning \
  --bucket $BUCKET \
  --versioning-configuration Status=Enabled

# Activer le chiffrement
aws s3api put-bucket-encryption \
  --bucket $BUCKET \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Créer la table DynamoDB
echo "🗄️  Création de la table DynamoDB..."
aws dynamodb create-table \
  --table-name $TABLE \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region $REGION 2>/dev/null || echo "  Table existe déjà"

echo "✅ Backend configuré !"
