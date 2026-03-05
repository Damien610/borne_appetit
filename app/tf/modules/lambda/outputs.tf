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
