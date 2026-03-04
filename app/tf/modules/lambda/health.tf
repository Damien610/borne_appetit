resource "aws_lambda_function" "health" {
  filename      = "${path.module}/../../../src/lambda/health.zip"
  function_name = "borne-appetit-health"
  role          = var.lambda_role_arn
  handler       = "health_handler.health"
  runtime       = "python3.11"
  
  source_code_hash = data.archive_file.health.output_base64sha256
}

data "archive_file" "health" {
  type        = "zip"
  source_file = "${path.module}/../../../src/infrastructure/health_handler.py"
  output_path = "${path.module}/../../../src/lambda/health.zip"
}

output "health_function_name" {
  value = aws_lambda_function.health.function_name
}

output "health_invoke_arn" {
  value = aws_lambda_function.health.invoke_arn
}
