resource "aws_lambda_function" "customer_lookup" {
  filename         = var.lambda_zip_path
  function_name    = "${var.project_name}-customer-lookup"
  role            = var.lambda_role_arn
  handler         = "infrastructure.customer_handler.handler"
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      CUSTOMERS_TABLE_NAME = var.customers_table_name
    }
  }
}

resource "aws_lambda_permission" "customer_lookup_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.customer_lookup.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}
