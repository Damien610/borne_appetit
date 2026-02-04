# Configuration des tables DynamoDB

# Table pour les produits et menus
resource "aws_dynamodb_table" "borne_appetit" {
  name           = "borne-appetit-table"
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

  global_secondary_index {
    name            = "TypeIndex"
    hash_key        = "Type"
    range_key       = "SK"
    projection_type = "ALL"
  }

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name = "Borne Appetit Table"
  }
}

# Table pour la configuration restaurant et terminaux
resource "aws_dynamodb_table" "config" {
  name           = "borne-appetit-config"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PK"
  range_key      = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name = "Borne Appetit Config"
  }
}
