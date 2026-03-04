output "config_table_name" {
  value = aws_dynamodb_table.config.name
}

output "config_table_arn" {
  value = aws_dynamodb_table.config.arn
}

output "customers_table_name" {
  value = aws_dynamodb_table.customers.name
}

output "customers_table_arn" {
  value = aws_dynamodb_table.customers.arn
}
