# Lambda Layer - Build automatique avec Docker
resource "null_resource" "build_shared_layer" {
  triggers = {
    infrastructure = filemd5("${path.module}/../../../src/infrastructure/dynamodb_repositories.py")
    application    = filemd5("${path.module}/../../../src/application/use_cases.py")
    domain         = filemd5("${path.module}/../../../src/domain/customer.py")
    requirements   = filemd5("${path.module}/../../../src/lambda/wallet/requirements.txt")
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      cd ${path.module}/../../..
      bash build_shared_layer.sh
    EOT
  }
}

resource "aws_lambda_layer_version" "shared_layer" {
  filename            = "${path.module}/../../../src/lambda/shared_layer.zip"
  layer_name          = "${var.project_name}-shared-layer"
  compatible_runtimes = ["python3.11"]
  source_code_hash    = filebase64sha256("${path.module}/../../../src/lambda/shared_layer.zip")
  
  depends_on = [null_resource.build_shared_layer]
}

output "shared_layer_arn" {
  value = aws_lambda_layer_version.shared_layer.arn
}
