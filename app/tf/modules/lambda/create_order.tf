data "archive_file" "create_order" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/restaurant/uuid/create_order"
  output_path = "${path.module}/.terraform/lambda_zips/create_order.zip"
}

resource "aws_lambda_function" "create_order" {
  filename      = data.archive_file.create_order.output_path
  function_name = "borne-appetit-create-order"
  role          = var.lambda_role_arn
  handler       = "create_order.handler"
  runtime       = "python3.11"
  timeout       = 30

  layers = [aws_lambda_layer_version.shared_layer.arn]

  environment {
    variables = {
      ORDER_TABLE_NAME = var.order_table_name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/restaurant/uuid/create_order/create_order.py")
}

resource "aws_lambda_permission" "create_order_api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_order.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_execution_arn}/*/*"
}

output "create_order_function_name" {
  value = aws_lambda_function.create_order.function_name
}

output "create_order_invoke_arn" {
  value = aws_lambda_function.create_order.invoke_arn
}
