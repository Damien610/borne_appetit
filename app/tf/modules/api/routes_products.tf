resource "aws_apigatewayv2_integration" "products_lookup" {
  api_id             = var.api_id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.products_lookup_invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "products_lookup" {
  api_id    = var.api_id
  route_key = "GET /restaurant/{restaurant_uuid}/products"
  target    = "integrations/${aws_apigatewayv2_integration.products_lookup.id}"
}
