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

variable "send_loyalty_card_function_name" {
  description = "Nom de la fonction Lambda send_loyalty_card"
  type        = string
}

variable "send_loyalty_card_invoke_arn" {
  description = "ARN d'invocation de la fonction Lambda send_loyalty_card"
  type        = string
}

variable "refresh_token_function_name" {
  description = "Nom de la fonction Lambda refresh_token"
  type        = string
}

variable "refresh_token_invoke_arn" {
  description = "ARN d'invocation de la fonction Lambda refresh_token"
  type        = string
}

variable "customer_lookup_function_name" {
  description = "Nom de la fonction Lambda customer_lookup"
  type        = string
}

variable "customer_lookup_invoke_arn" {
  description = "ARN d'invocation de la fonction Lambda customer_lookup"
  type        = string
}

variable "create_wallet_class_function_name" {
  description = "Nom de la fonction Lambda create_wallet_class"
  type        = string
}

variable "create_wallet_class_invoke_arn" {
  description = "ARN d'invocation de la fonction Lambda create_wallet_class"
  type        = string
}

variable "update_loyalty_points_function_name" {
  description = "Nom de la fonction Lambda update_loyalty_points"
  type        = string
}

variable "update_loyalty_points_invoke_arn" {
  description = "ARN d'invocation de la fonction Lambda update_loyalty_points"
  type        = string
}
