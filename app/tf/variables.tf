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