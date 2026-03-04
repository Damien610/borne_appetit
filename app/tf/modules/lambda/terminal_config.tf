resource "aws_lambda_function" "terminal_config" {
  filename      = "${path.module}/../../../src/lambda/terminal_config.zip"
  function_name = "borne-appetit-terminal-config"
  role          = var.lambda_role_arn
  handler       = "terminal_handler.handler"
  runtime       = "python3.11"
  
  environment {
    variables = {
      CONFIG_TABLE_NAME = var.config_table_name
    }
  }
  
  source_code_hash = data.archive_file.terminal_config.output_base64sha256
}

data "archive_file" "terminal_config" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src"
  output_path = "${path.module}/../../../src/lambda/terminal_config.zip"
}

output "terminal_config_function_name" {
  value = aws_lambda_function.terminal_config.function_name
}

output "terminal_config_invoke_arn" {
  value = aws_lambda_function.terminal_config.invoke_arn
}
