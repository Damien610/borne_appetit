data "archive_file" "customer_lookup" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src"
  output_path = "${path.module}/../../../src/lambda/customer_lookup.zip"
}

resource "aws_lambda_function" "customer_lookup" {
  filename         = data.archive_file.customer_lookup.output_path
  function_name    = "${var.project_name}-customer-lookup"
  role            = var.lambda_role_arn
  handler         = "infrastructure.customer_handler.handler"
  source_code_hash = data.archive_file.customer_lookup.output_base64sha256
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
