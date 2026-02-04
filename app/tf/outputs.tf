# Outputs de l'infrastructure
output "api_gateway_url" {
  description = "URL de l'API Gateway"
  value       = aws_apigatewayv2_api.api.api_endpoint
}

output "cloudfront_domain_name" {
  description = "URL CloudFront"
  value       = aws_cloudfront_distribution.cdn.domain_name
}

output "cloudfront_distribution_id" {
  description = "ID de la distribution CloudFront"
  value       = aws_cloudfront_distribution.cdn.id
}

output "s3_bucket_name" {
  description = "Nom du bucket S3"
  value       = aws_s3_bucket.assets.id
}

output "dynamodb_table_name" {
  description = "Nom de la table DynamoDB produits"
  value       = aws_dynamodb_table.borne_appetit.name
}

output "dynamodb_table_arn" {
  description = "ARN de la table DynamoDB produits"
  value       = aws_dynamodb_table.borne_appetit.arn
}

output "dynamodb_config_table_name" {
  description = "Nom de la table DynamoDB config"
  value       = aws_dynamodb_table.config.name
}

output "dynamodb_config_table_arn" {
  description = "ARN de la table DynamoDB config"
  value       = aws_dynamodb_table.config.arn
}

output "aws_region" {
  description = "Région AWS utilisée"
  value       = var.aws_region
}
