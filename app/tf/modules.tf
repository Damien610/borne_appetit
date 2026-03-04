# Module Database
module "database" {
  source = "./modules/database"
  
  project_name = var.project_name
}

# Module Lambda
module "lambda" {
  source = "./modules/lambda"
  
  lambda_role_arn           = aws_iam_role.lambda.arn
  config_table_name         = module.database.config_table_name
  customers_table_name      = module.database.customers_table_name
  smtp_user                 = var.smtp_user
  smtp_password             = var.smtp_password
  jwt_secret                = var.jwt_secret
  project_name              = var.project_name
  lambda_zip_path           = var.lambda_zip_path
  api_gateway_execution_arn = module.api_gateway.api_execution_arn
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
  send_loyalty_card_function_name   = module.lambda.send_loyalty_card_function_name
  send_loyalty_card_invoke_arn      = module.lambda.send_loyalty_card_invoke_arn
  refresh_token_function_name       = module.lambda.refresh_token_function_name
  refresh_token_invoke_arn          = module.lambda.refresh_token_invoke_arn
}

# Module Storage
module "storage" {
  source = "./modules/storage"
  
  bucket_name          = var.bucket_name
  domain_name          = var.domain_name
  acm_certificate_arn  = var.acm_certificate_arn
}
