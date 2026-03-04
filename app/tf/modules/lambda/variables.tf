variable "lambda_role_arn" {
  description = "ARN du rôle IAM pour les fonctions Lambda"
  type        = string
}

variable "config_table_name" {
  description = "Nom de la table DynamoDB de configuration"
  type        = string
}
