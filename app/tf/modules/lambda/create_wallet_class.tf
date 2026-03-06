data "archive_file" "create_wallet_class" {
  type        = "zip"
  source_file = "${path.module}/../../../src/lambda/wallet/post_wallet.py"
  output_path = "${path.module}/.terraform/lambda_zips/create_wallet_class.zip"
}

resource "aws_lambda_function" "create_wallet_class" {
  filename      = data.archive_file.create_wallet_class.output_path
  function_name = "borne-appetit-create-wallet-class"
  role          = var.lambda_role_arn
  handler       = "post_wallet.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30
  
  layers = [aws_lambda_layer_version.shared_layer.arn]
  
  environment {
    variables = {
      CONFIG_TABLE_NAME = var.config_table_name
      GOOGLE_WALLET_ISSUER_ID = var.google_wallet_issuer_id
      GOOGLE_WALLET_SERVICE_ACCOUNT = var.google_wallet_credentials
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/wallet/post_wallet.py")
}

resource "aws_lambda_permission" "create_wallet_class_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_wallet_class.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

output "create_wallet_class_function_name" {
  value = aws_lambda_function.create_wallet_class.function_name
}

output "create_wallet_class_invoke_arn" {
  value = aws_lambda_function.create_wallet_class.invoke_arn
}
