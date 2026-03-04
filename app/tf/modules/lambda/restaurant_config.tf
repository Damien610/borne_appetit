resource "aws_lambda_function" "restaurant_config" {
  filename      = "${path.module}/../../../src/lambda/restaurant_config.zip"
  function_name = "borne-appetit-restaurant-config"
  role          = var.lambda_role_arn
  handler       = "restaurant_handler.handler"
  runtime       = "python3.11"
  
  environment {
    variables = {
      CONFIG_TABLE_NAME = var.config_table_name
    }
  }
  
  source_code_hash = data.archive_file.restaurant_config.output_base64sha256
}

data "archive_file" "restaurant_config" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src"
  output_path = "${path.module}/../../../src/lambda/restaurant_config.zip"
}

output "restaurant_config_function_name" {
  value = aws_lambda_function.restaurant_config.function_name
}

output "restaurant_config_invoke_arn" {
  value = aws_lambda_function.restaurant_config.invoke_arn
}
