resource "aws_lambda_function" "update_loyalty_points" {
  filename         = var.lambda_zip_path
  function_name    = "${var.project_name}-update-loyalty-points"
  role            = var.lambda_role_arn
  handler         = "infrastructure.update_loyalty_points_handler.lambda_handler"
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      CUSTOMERS_TABLE_NAME           = var.customers_table_name
      JWT_SECRET                     = var.jwt_secret
      GOOGLE_WALLET_ISSUER_ID        = var.google_wallet_issuer_id
      GOOGLE_WALLET_SERVICE_ACCOUNT  = var.google_wallet_credentials
    }
  }
}

resource "aws_lambda_permission" "update_loyalty_points_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_loyalty_points.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}
