data "archive_file" "refresh_token" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/terminal/refresh_token"
  output_path = "${path.module}/.terraform/lambda_zips/refresh_token.zip"
  
  excludes = [
    "requirements.txt",
    "__pycache__",
    "*.pyc",
    "jwt",
    "jwt-*",
    "PyJWT-*",
    "cryptography",
    "cryptography-*",
    "google",
    "google_auth-*",
    "boto3",
    "boto3-*",
    "botocore",
    "botocore-*"
  ]
}

resource "aws_lambda_function" "refresh_token" {
  filename      = data.archive_file.refresh_token.output_path
  function_name = "borne-appetit-refresh-token"
  role          = var.lambda_role_arn
  handler       = "refresh_token.lambda_handler"
  runtime       = "python3.11"
  timeout       = 10
  
  layers = [aws_lambda_layer_version.shared_layer.arn]
  
  environment {
    variables = {
      CONFIG_TABLE_NAME = var.config_table_name
      JWT_SECRET = var.jwt_secret
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/terminal/refresh_token/refresh_token.py")
}

resource "aws_lambda_permission" "refresh_token_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.refresh_token.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

output "refresh_token_function_name" {
  value = aws_lambda_function.refresh_token.function_name
}

output "refresh_token_invoke_arn" {
  value = aws_lambda_function.refresh_token.invoke_arn
}
