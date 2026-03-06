data "archive_file" "send_loyalty_card" {
  type        = "zip"
  source_file = "${path.module}/../../../src/lambda/wallet/send_loyalty_card.py"
  output_path = "${path.module}/../../../src/lambda/wallet/send_loyalty_card.zip"
}

resource "aws_lambda_function" "send_loyalty_card" {
  filename      = data.archive_file.send_loyalty_card.output_path
  function_name = "borne-appetit-send-loyalty-card"
  role          = var.lambda_role_arn
  handler       = "send_loyalty_card.handler"
  runtime       = "python3.11"
  timeout       = 30
  
  layers = [aws_lambda_layer_version.shared_layer.arn]
  
  environment {
    variables = {
      SMTP_USER = var.smtp_user
      SMTP_PASSWORD = var.smtp_password
      CUSTOMERS_TABLE_NAME = var.customers_table_name
      CONFIG_TABLE_NAME = var.config_table_name
      JWT_SECRET = var.jwt_secret
      GOOGLE_WALLET_ISSUER_ID = var.google_wallet_issuer_id
      GOOGLE_WALLET_SERVICE_ACCOUNT = var.google_wallet_credentials
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/wallet/send_loyalty_card.py")
}

resource "aws_lambda_permission" "send_loyalty_card_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.send_loyalty_card.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

output "send_loyalty_card_function_name" {
  value = aws_lambda_function.send_loyalty_card.function_name
}

output "send_loyalty_card_invoke_arn" {
  value = aws_lambda_function.send_loyalty_card.invoke_arn
}
