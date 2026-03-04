#!/bin/bash
set -e

echo "🚀 Déploiement Backend Borne Appétit"

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip install -r src/lambda/requirements.txt -t src/lambda/auth/
pip install -r src/lambda/requirements.txt -t src/lambda/products/
pip install -r src/lambda/requirements.txt -t src/lambda/orders/
pip install -r src/lambda/requirements.txt -t src/lambda/loyalty/

# Terraform
echo "🏗️  Déploiement infrastructure..."
cd tf
terraform init
terraform plan
terraform apply -auto-approve

echo "✅ Déploiement terminé!"
echo "📝 URL API: $(terraform output -raw api_url)"
