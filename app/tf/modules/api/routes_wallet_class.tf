resource "aws_apigatewayv2_route" "create_wallet_class" {
  api_id    = var.api_id
  route_key = "POST /wallet/class/{restaurant_id}"
  target    = "integrations/${aws_apigatewayv2_integration.create_wallet_class.id}"
}

resource "aws_apigatewayv2_integration" "create_wallet_class" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"
  integration_uri  = var.create_wallet_class_invoke_arn
}
