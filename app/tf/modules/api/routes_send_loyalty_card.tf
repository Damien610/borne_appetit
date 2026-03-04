resource "aws_apigatewayv2_route" "send_loyalty_card" {
  api_id    = var.api_id
  route_key = "POST /send-loyalty-card"
  target    = "integrations/${aws_apigatewayv2_integration.send_loyalty_card.id}"
}

resource "aws_apigatewayv2_integration" "send_loyalty_card" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"
  integration_uri  = var.send_loyalty_card_invoke_arn
}
