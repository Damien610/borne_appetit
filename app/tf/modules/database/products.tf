# Configuration des tables DynamoDB

# Table pour la configuration des produits
resource "aws_dynamodb_table" "products" {
  name           = "borne-appetit-products"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PK"
  range_key      = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

   attribute {
    name = "name"
    type = "S"
  }

   attribute {
    name = "price"
    type = "N"
  }

   attribute {
    name = "category_name"
    type = "S"
  }

  global_secondary_index {
    name            = "uri_name-index"
    hash_key        = "name"
    projection_type = "ALL"
  }

   global_secondary_index {
    name            = "uri_price-index"
    hash_key        = "price"
    projection_type = "ALL"
  }

   global_secondary_index {
    name            = "uri_category_name-index"
    hash_key        = "category_name"
    projection_type = "ALL"
  }

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name = "Borne Appetit Products"
  }
}