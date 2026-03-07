data "archive_file" "customer_lookup" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/restaurant/uuid/get_costumer"
  output_path = "${path.module}/.terraform/lambda_zips/customer_lookup.zip"
}

resource "aws_lambda_function" "customer_lookup" {
  filename      = data.archive_file.customer_lookup.output_path
  function_name = "borne-appetit-customer-lookup"
  role          = var.lambda_role_arn
  handler       = "get_costumer.handler"
  runtime       = "python3.11"
  timeout       = 30
  
  layers = [aws_lambda_layer_version.shared_layer.arn]
  
  environment {
    variables = {
      CUSTOMERS_TABLE_NAME = var.customers_table_name
    }
  }

  source_code_hash = data.archive_file.customer_lookup.output_base64sha256
}

resource "aws_lambda_permission" "customer_lookup_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.customer_lookup.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

output "customer_lookup_function_name" {
  value = aws_lambda_function.customer_lookup.function_name
}

output "customer_lookup_invoke_arn" {
  value = aws_lambda_function.customer_lookup.invoke_arn
}
