# Configuration de l'API Gateway
resource "aws_apigatewayv2_api" "api" {
  name          = "borne-appetit-api"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["*"]
    max_age       = 300
  }
}

resource "aws_apigatewayv2_stage" "api" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}

# Route /health
resource "aws_apigatewayv2_integration" "health" {
  api_id           = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.health.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "health" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /health"
  target    = "integrations/${aws_apigatewayv2_integration.health.id}"
}

resource "aws_lambda_permission" "health" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.health.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}

# Route /terminal/config/{uuid}
resource "aws_apigatewayv2_integration" "terminal_config" {
  api_id           = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.terminal_config.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "terminal_config" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /terminal/config/{uuid}"
  target    = "integrations/${aws_apigatewayv2_integration.terminal_config.id}"
}

resource "aws_lambda_permission" "terminal_config" {
  statement_id  = "AllowAPIGatewayInvokeTerminalConfig"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.terminal_config.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}

# Route /{uri}/config
resource "aws_apigatewayv2_integration" "restaurant_config" {
  api_id           = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.restaurant_config.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "restaurant_config" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /restaurant/{uri}/config"
  target    = "integrations/${aws_apigatewayv2_integration.restaurant_config.id}"
}

resource "aws_lambda_permission" "restaurant_config" {
  statement_id  = "AllowAPIGatewayInvokeRestaurantConfig"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.restaurant_config.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}
