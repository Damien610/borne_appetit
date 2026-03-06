variable "products_table_name" {
  description = "Name of the DynamoDB products table"
  type        = string
}

data "archive_file" "products_lookup" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src"
  output_path = "${path.module}/products_lookup.zip"
}

resource "aws_lambda_function" "products_lookup" {
  filename         = data.archive_file.products_lookup.output_path
  function_name    = "${var.project_name}-products-class"
  role             = var.lambda_role_arn
  handler          = "infrastructure.products_lookup.lambda_handler"
  source_code_hash = data.archive_file.products_lookup.output_base64sha256
  runtime          = "python3.11"
  timeout          = 30

  environment {
    variables = {
      PRODUCTS_TABLE_NAME = var.products_table_name
    }
  }
}

resource "aws_lambda_permission" "products_lookup_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.products_lookup.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

