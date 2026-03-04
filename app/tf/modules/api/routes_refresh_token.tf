resource "aws_apigatewayv2_route" "refresh_token" {
  api_id    = var.api_id
  route_key = "POST /terminal/refresh-token"
  target    = "integrations/${aws_apigatewayv2_integration.refresh_token.id}"
}

resource "aws_apigatewayv2_integration" "refresh_token" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"
  integration_uri  = var.refresh_token_invoke_arn
}
