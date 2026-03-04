resource "aws_dynamodb_table" "customers" {
  name           = "${var.project_name}-customers"
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
    name = "loyalty_code"
    type = "S"
  }

  attribute {
    name = "restaurant_email"
    type = "S"
  }

  global_secondary_index {
    name            = "LoyaltyCodeIndex"
    hash_key        = "loyalty_code"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "RestaurantEmailIndex"
    hash_key        = "restaurant_email"
    projection_type = "ALL"
  }

  tags = {
    Name = "${var.project_name}-customers"
  }
}
