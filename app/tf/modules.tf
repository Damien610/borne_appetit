# Module Database
module "database" {
  source = "./modules/database"
}

# Module Lambda
module "lambda" {
  source = "./modules/lambda"
  
  lambda_role_arn    = aws_iam_role.lambda.arn
  config_table_name  = module.database.config_table_name
}

# Module API Gateway
module "api_gateway" {
  source = "./modules/api"
  
  api_id           = module.api_gateway.api_id
  api_execution_arn = module.api_gateway.api_execution_arn
  
  health_function_name              = module.lambda.health_function_name
  health_invoke_arn                 = module.lambda.health_invoke_arn
  terminal_config_function_name     = module.lambda.terminal_config_function_name
  terminal_config_invoke_arn        = module.lambda.terminal_config_invoke_arn
  restaurant_config_function_name   = module.lambda.restaurant_config_function_name
  restaurant_config_invoke_arn      = module.lambda.restaurant_config_invoke_arn
}

# Module Storage
module "storage" {
  source = "./modules/storage"
  
  bucket_name          = var.bucket_name
  domain_name          = var.domain_name
  acm_certificate_arn  = var.acm_certificate_arn
}
