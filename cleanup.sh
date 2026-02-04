#!/bin/bash
set -e

REGION="eu-west-1"

echo "🧹 Nettoyage des ressources AWS..."

# CloudFront (doit être désactivé avant suppression)
echo "📦 Recherche des distributions CloudFront..."
DISTRIBUTIONS=$(aws cloudfront list-distributions --query "DistributionList.Items[?Comment=='Borne Appetit CDN'].Id" --output text 2>/dev/null || true)
if [ -n "$DISTRIBUTIONS" ]; then
  for DIST_ID in $DISTRIBUTIONS; do
    echo "  Désactivation de $DIST_ID..."
    ETAG=$(aws cloudfront get-distribution-config --id $DIST_ID --query 'ETag' --output text)
    aws cloudfront get-distribution-config --id $DIST_ID --query 'DistributionConfig' > /tmp/dist-config.json
    jq '.Enabled = false' /tmp/dist-config.json > /tmp/dist-config-disabled.json
    aws cloudfront update-distribution --id $DIST_ID --distribution-config file:///tmp/dist-config-disabled.json --if-match $ETAG
    echo "  ⚠️  Attendre que CloudFront soit désactivé avant de supprimer (peut prendre 15-20 min)"
  done
fi

# Lambda functions
echo "⚡ Suppression des fonctions Lambda..."
for FUNC in borne-appetit-get-menu borne-appetit-create-order borne-appetit-get-orders; do
  aws lambda delete-function --function-name $FUNC --region $REGION 2>/dev/null && echo "  ✓ $FUNC" || echo "  ⊘ $FUNC (n'existe pas)"
done

# API Gateway
echo "🌐 Suppression de l'API Gateway..."
API_ID=$(aws apigatewayv2 get-apis --region $REGION --query "Items[?Name=='borne-appetit-api'].ApiId" --output text 2>/dev/null || true)
if [ -n "$API_ID" ]; then
  aws apigatewayv2 delete-api --api-id $API_ID --region $REGION && echo "  ✓ API supprimée"
fi

# S3 buckets (vider puis supprimer)
echo "🪣 Suppression des buckets S3..."
for BUCKET in borne-appetit-assets borne-appetit-terraform-state; do
  if aws s3 ls s3://$BUCKET 2>/dev/null; then
    aws s3 rm s3://$BUCKET --recursive 2>/dev/null || true
    aws s3 rb s3://$BUCKET --force 2>/dev/null && echo "  ✓ $BUCKET" || echo "  ✗ $BUCKET"
  else
    echo "  ⊘ $BUCKET (n'existe pas)"
  fi
done

# DynamoDB tables
echo "🗄️  Suppression des tables DynamoDB..."
for TABLE in borne-appetit-table borne-appetit-config borne-appetit-terraform-locks; do
  aws dynamodb delete-table --table-name $TABLE --region $REGION 2>/dev/null && echo "  ✓ $TABLE" || echo "  ⊘ $TABLE (n'existe pas)"
done

# IAM role et policies
echo "👤 Suppression du rôle IAM..."
ROLE_NAME="borne-appetit-lambda-role"
POLICIES=$(aws iam list-attached-role-policies --role-name $ROLE_NAME --query 'AttachedPolicies[].PolicyArn' --output text 2>/dev/null || true)
if [ -n "$POLICIES" ]; then
  for POLICY in $POLICIES; do
    aws iam detach-role-policy --role-name $ROLE_NAME --policy-arn $POLICY 2>/dev/null
  done
fi
aws iam delete-role --role-name $ROLE_NAME 2>/dev/null && echo "  ✓ $ROLE_NAME" || echo "  ⊘ $ROLE_NAME (n'existe pas)"

# CloudFront OAI
echo "🔐 Suppression des OAI CloudFront..."
OAI_IDS=$(aws cloudfront list-cloud-front-origin-access-identities --query "CloudFrontOriginAccessIdentityList.Items[?Comment=='OAI for Borne Appetit'].Id" --output text 2>/dev/null || true)
if [ -n "$OAI_IDS" ]; then
  for OAI_ID in $OAI_IDS; do
    ETAG=$(aws cloudfront get-cloud-front-origin-access-identity --id $OAI_ID --query 'ETag' --output text)
    aws cloudfront delete-cloud-front-origin-access-identity --id $OAI_ID --if-match $ETAG 2>/dev/null && echo "  ✓ $OAI_ID" || echo "  ✗ $OAI_ID"
  done
fi

echo ""
echo "✅ Nettoyage terminé !"
echo ""
echo "⚠️  Si des distributions CloudFront ont été désactivées, attendez 15-20 minutes puis exécutez :"
echo "    aws cloudfront delete-distribution --id <DIST_ID> --if-match <ETAG>"
