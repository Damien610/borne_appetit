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

output "products_table_name" {
  value = aws_dynamodb_table.products.name
}

output "products_table_arn" {
  value = aws_dynamodb_table.products.arn
}

output "order_table_name" {
  value = aws_dynamodb_table.order.name
}

output "order_table_arn" {
  value = aws_dynamodb_table.order.arn
}