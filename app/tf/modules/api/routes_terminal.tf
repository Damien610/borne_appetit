resource "aws_apigatewayv2_integration" "terminal_config" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"
  integration_uri  = var.terminal_config_invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "terminal_config" {
  api_id    = var.api_id
  route_key = "GET /terminal/config/{uuid}"
  target    = "integrations/${aws_apigatewayv2_integration.terminal_config.id}"
}

resource "aws_lambda_permission" "terminal_config" {
  statement_id  = "AllowAPIGatewayInvokeTerminalConfig"
  action        = "lambda:InvokeFunction"
  function_name = var.terminal_config_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}
