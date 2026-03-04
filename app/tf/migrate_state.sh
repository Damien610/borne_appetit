#!/bin/bash

# Migration du state vers la nouvelle structure modulaire

# S3 Bucket
terraform state mv aws_s3_bucket.assets module.storage.aws_s3_bucket.assets 2>/dev/null || echo "S3 bucket déjà migré ou n'existe pas"

# CloudFront OAI
terraform state mv aws_cloudfront_origin_access_identity.oai module.storage.aws_cloudfront_origin_access_identity.oai 2>/dev/null || echo "CloudFront OAI déjà migré"

# Import DynamoDB si elle existe
terraform import module.database.aws_dynamodb_table.config borne-appetit-config 2>/dev/null || echo "DynamoDB déjà importée"

echo "Migration terminée"
