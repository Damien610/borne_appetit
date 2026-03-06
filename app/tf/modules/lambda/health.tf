data "archive_file" "health" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/health"
  output_path = "${path.module}/../../../src/lambda/health/health.zip"
}

resource "aws_lambda_function" "health" {
  filename      = data.archive_file.health.output_path
  function_name = "borne-appetit-health"
  role          = var.lambda_role_arn
  handler       = "health.handler"
  runtime       = "python3.11"
  timeout       = 3
  
  layers = [aws_lambda_layer_version.shared_layer.arn]
  
  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/health/health.py")
}

output "health_function_name" {
  value = aws_lambda_function.health.function_name
}

output "health_invoke_arn" {
  value = aws_lambda_function.health.invoke_arn
}
