variable "bucket_name" {
  description = "Nom du bucket S3"
  type        = string
}

variable "domain_name" {
  description = "Nom de domaine personnalisé"
  type        = string
  default     = ""
}

variable "acm_certificate_arn" {
  description = "ARN du certificat ACM"
  type        = string
  default     = ""
}
