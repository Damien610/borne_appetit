resource "aws_apigatewayv2_integration" "create_order" {
  api_id             = var.api_id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.create_order_invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "create_order" {
  api_id    = var.api_id
  route_key = "POST /restaurant/{restaurant_uuid}/order"
  target    = "integrations/${aws_apigatewayv2_integration.create_order.id}"
}
