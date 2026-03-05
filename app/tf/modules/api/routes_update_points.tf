resource "aws_apigatewayv2_route" "update_loyalty_points" {
  api_id    = var.api_id
  route_key = "PATCH /customer/{customer_id}/points"
  target    = "integrations/${aws_apigatewayv2_integration.update_loyalty_points.id}"
}

resource "aws_apigatewayv2_integration" "update_loyalty_points" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"
  integration_uri  = var.update_loyalty_points_invoke_arn
}
