# Outputs de l'infrastructure
output "api_gateway_url" {
  description = "URL de l'API Gateway"
  value       = module.api_gateway.api_endpoint
}

output "cloudfront_domain_name" {
  description = "URL CloudFront"
  value       = module.storage.cloudfront_domain_name
}

output "cloudfront_distribution_id" {
  description = "ID de la distribution CloudFront"
  value       = module.storage.cloudfront_distribution_id
}

output "s3_bucket_name" {
  description = "Nom du bucket S3"
  value       = module.storage.s3_bucket_name
}

output "dynamodb_config_table_name" {
  description = "Nom de la table DynamoDB config"
  value       = module.database.config_table_name
}

output "dynamodb_config_table_arn" {
  description = "ARN de la table DynamoDB config"
  value       = module.database.config_table_arn
}

output "aws_region" {
  description = "Région AWS utilisée"
  value       = var.aws_region
}
