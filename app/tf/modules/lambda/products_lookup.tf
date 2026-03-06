data "archive_file" "products_lookup" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/restaurant/uuid/get_products"
  output_path = "${path.module}/../../../src/lambda/restaurant/uuid/get_products/products_lookup.zip"
}

resource "aws_lambda_function" "products_lookup" {
  filename      = data.archive_file.products_lookup.output_path
  function_name = "borne-appetit-products-class"
  role          = var.lambda_role_arn
  handler       = "get_products.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30
  
  layers = [aws_lambda_layer_version.shared_layer.arn]
  
  environment {
    variables = {
      PRODUCTS_TABLE_NAME = var.products_table_name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/restaurant/uuid/get_products/get_products.py")
}

resource "aws_lambda_permission" "products_lookup_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.products_lookup.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

output "products_lookup_function_name" {
  value = aws_lambda_function.products_lookup.function_name
}

output "products_lookup_invoke_arn" {
  value = aws_lambda_function.products_lookup.invoke_arn
}
