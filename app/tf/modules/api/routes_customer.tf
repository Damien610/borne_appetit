resource "aws_apigatewayv2_integration" "customer_lookup" {
  api_id             = var.api_id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.customer_lookup_invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "customer_lookup" {
  api_id    = var.api_id
  route_key = "GET /restaurant/{restaurant_uuid}/customer"
  target    = "integrations/${aws_apigatewayv2_integration.customer_lookup.id}"
}
