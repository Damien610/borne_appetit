#!/bin/bash
set -e

cd app/tf

echo "📥 Import des ressources existantes dans Terraform..."

# DynamoDB Tables
terraform import aws_dynamodb_table.borne_appetit borne-appetit-table 2>/dev/null || echo "  Déjà importé: borne-appetit-table"
terraform import aws_dynamodb_table.config borne-appetit-config 2>/dev/null || echo "  Déjà importé: borne-appetit-config"

# IAM Role
terraform import aws_iam_role.lambda borne-appetit-lambda-role 2>/dev/null || echo "  Déjà importé: lambda role"

# S3 Bucket
terraform import aws_s3_bucket.assets borne-appetit-assets 2>/dev/null || echo "  Déjà importé: assets bucket"

# Lambda Function
terraform import aws_lambda_function.health borne-appetit-health 2>/dev/null || echo "  Déjà importé: health function"

# Lambda Permission
terraform import aws_lambda_permission.health borne-appetit-health/AllowAPIGatewayInvoke 2>/dev/null || echo "  Déjà importé: lambda permission"

echo "✅ Import terminé ! Vous pouvez maintenant faire: terraform apply"
