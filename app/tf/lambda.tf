# Configuration des fonctions Lambda
resource "aws_lambda_function" "health" {
  filename      = "${path.module}/../src/lambda/health.zip"
  function_name = "borne-appetit-health"
  role          = aws_iam_role.lambda.arn
  handler       = "handler.health"
  runtime       = "python3.11"
  
  source_code_hash = data.archive_file.health.output_base64sha256
}

data "archive_file" "health" {
  type        = "zip"
  source_file = "${path.module}/../src/lambda/handler.py"
  output_path = "${path.module}/../src/lambda/health.zip"
}
