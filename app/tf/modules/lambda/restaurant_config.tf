data "archive_file" "restaurant_config" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/restaurant/uri/get_config"
  output_path = "${path.module}/../../../src/lambda/restaurant/uri/get_config/restaurant_config.zip"
}

resource "aws_lambda_function" "restaurant_config" {
  filename      = data.archive_file.restaurant_config.output_path
  function_name = "borne-appetit-restaurant-config"
  role          = var.lambda_role_arn
  handler       = "get_config.handler"
  runtime       = "python3.11"
  timeout       = 3
  
  layers = [aws_lambda_layer_version.shared_layer.arn]
  
  environment {
    variables = {
      CONFIG_TABLE_NAME = var.config_table_name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/restaurant/uri/get_config/get_config.py")
}

resource "aws_lambda_permission" "restaurant_config_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.restaurant_config.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

output "restaurant_config_function_name" {
  value = aws_lambda_function.restaurant_config.function_name
}

output "restaurant_config_invoke_arn" {
  value = aws_lambda_function.restaurant_config.invoke_arn
}
