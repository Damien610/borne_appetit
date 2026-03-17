variable "lambda_role_arn" {
  description = "ARN du rôle IAM pour les fonctions Lambda"
  type        = string
}

variable "config_table_name" {
  description = "Nom de la table DynamoDB de configuration"
  type        = string
}

variable "smtp_user" {
  description = "Email SMTP Google"
  type        = string
  sensitive   = true
}

variable "smtp_password" {
  description = "Mot de passe SMTP Google"
  type        = string
  sensitive   = true
}

variable "customers_table_name" {
  description = "Nom de la table DynamoDB customers"
  type        = string
}

variable "jwt_secret" {
  description = "Secret pour signer les JWT"
  type        = string
  sensitive   = true
}

variable "google_wallet_issuer_id" {
  description = "Google Wallet Issuer ID"
  type        = string
  sensitive   = true
}

variable "google_wallet_credentials" {
  description = "Google Wallet Service Account JSON"
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "api_gateway_execution_arn" {
  description = "ARN d'exécution de l'API Gateway"
  type        = string
}


variable "products_table_name" {
  description = "Nom de la table DynamoDB products"
  type        = string
}

variable "order_table_name" {
  description = "Nom de la table DynamoDB order"
  type        = string
}
