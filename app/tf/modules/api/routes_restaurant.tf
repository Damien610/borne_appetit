resource "aws_apigatewayv2_integration" "restaurant_config" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"
  integration_uri  = var.restaurant_config_invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "restaurant_config" {
  api_id    = var.api_id
  route_key = "GET /restaurant/{uri}/config"
  target    = "integrations/${aws_apigatewayv2_integration.restaurant_config.id}"
}

resource "aws_lambda_permission" "restaurant_config" {
  statement_id  = "AllowAPIGatewayInvokeRestaurantConfig"
  action        = "lambda:InvokeFunction"
  function_name = var.restaurant_config_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}
