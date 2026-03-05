variable "aws_region" {
  description = "Région AWS"
  type        = string
  default     = "eu-west-1"
}

variable "bucket_name" {
  description = "Nom du bucket S3"
  type        = string
  default     = "borne-appetit-assets"
}

variable "domain_name" {
  description = "Nom de domaine personnalisé (ex: assets.appetit.com)"
  type        = string
  default     = ""
}

variable "acm_certificate_arn" {
  description = "ARN du certificat ACM (doit être dans us-east-1)"
  type        = string
  default     = ""
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

variable "project_name" {
  description = "Nom du projet"
  type        = string
  default     = "borne-appetit"
}

variable "lambda_zip_path" {
  description = "Chemin vers le zip Lambda"
  type        = string
  default     = "../lambda.zip"
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