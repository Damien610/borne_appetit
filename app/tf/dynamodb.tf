# Configuration des tables DynamoDB
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

  attribute {
    name = "Type"
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
