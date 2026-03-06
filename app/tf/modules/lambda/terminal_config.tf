data "archive_file" "terminal_config" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/terminal/config"
  output_path = "${path.module}/../../../src/lambda/terminal/config/terminal_config.zip"
}

resource "aws_lambda_function" "terminal_config" {
  filename      = data.archive_file.terminal_config.output_path
  function_name = "borne-appetit-terminal-config"
  role          = var.lambda_role_arn
  handler       = "get_config.handler"
  runtime       = "python3.11"
  
  layers = [aws_lambda_layer_version.shared_layer.arn]
  
  environment {
    variables = {
      CONFIG_TABLE_NAME = var.config_table_name
    }
  }
  
  source_code_hash = filebase64sha256("${path.module}/../../../src/lambda/terminal/config/get_config.py")
}

output "terminal_config_function_name" {
  value = aws_lambda_function.terminal_config.function_name
}

output "terminal_config_invoke_arn" {
  value = aws_lambda_function.terminal_config.invoke_arn
}
