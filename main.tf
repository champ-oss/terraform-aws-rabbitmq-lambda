locals {
  tags = {
    cost    = "shared"
    creator = "terraform"
    git     = var.git
  }
}

data "aws_region" "this" {}

resource "random_id" "this" {
  count       = var.enabled ? 1 : 0
  byte_length = 3
}

data "archive_file" "this" {
  count            = var.enabled ? 1 : 0
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/src"
  output_path      = "${path.module}/package.zip"
}

module "this" {
  count                          = var.enabled ? 1 : 0
  source                         = "github.com/champ-oss/terraform-aws-lambda.git?ref=v1.0.143-ad06349"
  git                            = var.git
  name                           = "rabbitmq-lambda"
  tags                           = merge(local.tags, var.tags)
  runtime                        = var.runtime
  handler                        = "main.handler"
  filename                       = data.archive_file.this[0].output_path
  source_code_hash               = data.archive_file.this[0].output_base64sha256
  reserved_concurrent_executions = var.reserved_concurrent_executions
  environment = {
    "FOO" = "BAR"
  }
}
