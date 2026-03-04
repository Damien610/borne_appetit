variable "api_id" {
  description = "ID de l'API Gateway"
  type        = string
}

variable "api_execution_arn" {
  description = "ARN d'exécution de l'API Gateway"
  type        = string
}

variable "health_function_name" {
  description = "Nom de la fonction Lambda health"
  type        = string
}

variable "health_invoke_arn" {
  description = "ARN d'invocation de la fonction Lambda health"
  type        = string
}

variable "terminal_config_function_name" {
  description = "Nom de la fonction Lambda terminal_config"
  type        = string
}

variable "terminal_config_invoke_arn" {
  description = "ARN d'invocation de la fonction Lambda terminal_config"
  type        = string
}

variable "restaurant_config_function_name" {
  description = "Nom de la fonction Lambda restaurant_config"
  type        = string
}

variable "restaurant_config_invoke_arn" {
  description = "ARN d'invocation de la fonction Lambda restaurant_config"
  type        = string
}
