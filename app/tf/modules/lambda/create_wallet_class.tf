data "archive_file" "create_wallet_class" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src"
  output_path = "${path.module}/../../../src/lambda/create_wallet_class.zip"
}

resource "aws_lambda_function" "create_wallet_class" {
  filename         = data.archive_file.create_wallet_class.output_path
  function_name    = "${var.project_name}-create-wallet-class"
  role            = var.lambda_role_arn
  handler         = "infrastructure.create_wallet_class_handler.lambda_handler"
  source_code_hash = data.archive_file.create_wallet_class.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      CONFIG_TABLE_NAME              = var.config_table_name
      GOOGLE_WALLET_ISSUER_ID        = var.google_wallet_issuer_id
      GOOGLE_WALLET_SERVICE_ACCOUNT  = var.google_wallet_credentials
    }
  }
}

resource "aws_lambda_permission" "create_wallet_class_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_wallet_class.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}
