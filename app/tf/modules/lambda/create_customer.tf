data "archive_file" "create_customer" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/restaurant/uuid/create_customer"
  output_path = "${path.module}/.terraform/lambda_zips/create_customer.zip"
}

resource "aws_lambda_function" "create_customer" {
  filename      = data.archive_file.create_customer.output_path
  function_name = "borne-appetit-create-customer"
  role          = var.lambda_role_arn
  handler       = "create_customer.handler"
  runtime       = "python3.11"
  timeout       = 30

  layers = [aws_lambda_layer_version.shared_layer.arn]

  environment {
    variables = {
      CUSTOMERS_TABLE_NAME = var.customers_table_name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/restaurant/uuid/create_customer/create_customer.py")
}

resource "aws_lambda_permission" "create_customer_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_customer.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

output "create_customer_function_name" {
  value = aws_lambda_function.create_customer.function_name
}

output "create_customer_invoke_arn" {
  value = aws_lambda_function.create_customer.invoke_arn
}
