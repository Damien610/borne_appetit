data "archive_file" "update_loyalty_points" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/costumer/update_point"
  output_path = "${path.module}/../../../src/lambda/costumer/update_point/update_loyalty_points.zip"
}

resource "aws_lambda_function" "update_loyalty_points" {
  filename      = data.archive_file.update_loyalty_points.output_path
  function_name = "borne-appetit-update-loyalty-points"
  role          = var.lambda_role_arn
  handler       = "update_costumer_point.handler"
  runtime       = "python3.11"
  timeout       = 30
  
  layers = [aws_lambda_layer_version.shared_layer.arn]
  
  environment {
    variables = {
      CUSTOMERS_TABLE_NAME = var.customers_table_name
      JWT_SECRET = var.jwt_secret
      GOOGLE_WALLET_ISSUER_ID = var.google_wallet_issuer_id
      GOOGLE_WALLET_SERVICE_ACCOUNT = var.google_wallet_credentials
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/costumer/update_point/update_costumer_point.py")
}

resource "aws_lambda_permission" "update_loyalty_points_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_loyalty_points.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

output "update_loyalty_points_function_name" {
  value = aws_lambda_function.update_loyalty_points.function_name
}

output "update_loyalty_points_invoke_arn" {
  value = aws_lambda_function.update_loyalty_points.invoke_arn
}
