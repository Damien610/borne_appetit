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

resource "aws_lambda_function" "terminal_config" {
  filename      = "${path.module}/../src/lambda/terminal_config.zip"
  function_name = "borne-appetit-terminal-config"
  role          = aws_iam_role.lambda.arn
  handler       = "terminal_config.handler"
  runtime       = "python3.11"
  
  environment {
    variables = {
      CONFIG_TABLE_NAME = aws_dynamodb_table.config.name
    }
  }
  
  source_code_hash = data.archive_file.terminal_config.output_base64sha256
}

data "archive_file" "terminal_config" {
  type        = "zip"
  source_file = "${path.module}/../src/lambda/terminal_config.py"
  output_path = "${path.module}/../src/lambda/terminal_config.zip"
}
