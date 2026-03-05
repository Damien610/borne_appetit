data "archive_file" "refresh_token" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src"
  output_path = "${path.module}/../../../src/lambda/refresh_token.zip"
}

resource "aws_lambda_function" "refresh_token" {
  filename         = data.archive_file.refresh_token.output_path
  function_name    = "${var.project_name}-refresh-token"
  role            = var.lambda_role_arn
  handler         = "infrastructure.refresh_token_handler.lambda_handler"
  source_code_hash = data.archive_file.refresh_token.output_base64sha256
  runtime         = "python3.11"
  timeout         = 10

  environment {
    variables = {
      CONFIG_TABLE_NAME = var.config_table_name
      JWT_SECRET        = var.jwt_secret
    }
  }
}

resource "aws_lambda_permission" "refresh_token_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.refresh_token.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}
