output "send_loyalty_card_invoke_arn" {
  description = "ARN d'invocation de la Lambda send-loyalty-card"
  value       = aws_lambda_function.send_loyalty_card.invoke_arn
}

output "send_loyalty_card_function_name" {
  description = "Nom de la fonction Lambda send-loyalty-card"
  value       = aws_lambda_function.send_loyalty_card.function_name
}

output "refresh_token_invoke_arn" {
  description = "ARN d'invocation de la Lambda refresh-token"
  value       = aws_lambda_function.refresh_token.invoke_arn
}

output "refresh_token_function_name" {
  description = "Nom de la fonction Lambda refresh-token"
  value       = aws_lambda_function.refresh_token.function_name
}

output "customer_lookup_invoke_arn" {
  description = "ARN d'invocation de la Lambda customer-lookup"
  value       = aws_lambda_function.customer_lookup.invoke_arn
}

output "customer_lookup_function_name" {
  description = "Nom de la fonction Lambda customer-lookup"
  value       = aws_lambda_function.customer_lookup.function_name
}

output "create_wallet_class_invoke_arn" {
  description = "ARN d'invocation de la Lambda create-wallet-class"
  value       = aws_lambda_function.create_wallet_class.invoke_arn
}

output "create_wallet_class_function_name" {
  description = "Nom de la fonction Lambda create-wallet-class"
  value       = aws_lambda_function.create_wallet_class.function_name
}

output "update_loyalty_points_invoke_arn" {
  description = "ARN d'invocation de la Lambda update-loyalty-points"
  value       = aws_lambda_function.update_loyalty_points.invoke_arn
}

output "update_loyalty_points_function_name" {
  description = "Nom de la fonction Lambda update-loyalty-points"
  value       = aws_lambda_function.update_loyalty_points.function_name
}
