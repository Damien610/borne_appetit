# Lambda Layer
resource "aws_lambda_layer_version" "shared_layer" {
  filename            = "${path.module}/../../../src/lambda/shared_layer.zip"
  layer_name          = "${var.project_name}-shared-layer"
  compatible_runtimes = ["python3.11"]
  source_code_hash    = filebase64sha256("${path.module}/../../../src/lambda/shared_layer.zip")
}

output "shared_layer_arn" {
  value = aws_lambda_layer_version.shared_layer.arn
}
