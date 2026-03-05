data "archive_file" "send_loyalty_card" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src"
  output_path = "${path.module}/../../../src/lambda/send_loyalty_card.zip"
}

resource "aws_lambda_function" "send_loyalty_card" {
  filename         = data.archive_file.send_loyalty_card.output_path
  function_name    = "${var.project_name}-send-loyalty-card"
  role            = var.lambda_role_arn
  handler         = "infrastructure.send_loyalty_card_handler.lambda_handler"
  source_code_hash = data.archive_file.send_loyalty_card.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      SMTP_USER                      = var.smtp_user
      SMTP_PASSWORD                  = var.smtp_password
      CUSTOMERS_TABLE_NAME           = var.customers_table_name
      CONFIG_TABLE_NAME              = var.config_table_name
      JWT_SECRET                     = var.jwt_secret
      GOOGLE_WALLET_ISSUER_ID        = var.google_wallet_issuer_id
      GOOGLE_WALLET_SERVICE_ACCOUNT  = var.google_wallet_credentials
    }
  }
}

resource "aws_lambda_permission" "send_loyalty_card_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.send_loyalty_card.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}
