locals {
  tags = {
    cost    = "shared"
    creator = "terraform"
    git     = var.git
  }
}

data "aws_region" "this" {
  count = var.enabled ? 1 : 0
}

resource "random_id" "this" {
  byte_length = 3
}

module "hash" {
  source   = "github.com/champ-oss/terraform-git-hash.git?ref=v1.0.15-cd75e35"
  path     = path.module
  fallback = ""
}

module "this" {
  source                         = "github.com/champ-oss/terraform-aws-lambda.git?ref=v1.0.147-dd45619"
  enabled                        = var.enabled
  git                            = var.git
  name                           = "rabbitmq-lambda"
  tags                           = merge(local.tags, var.tags)
  memory_size                    = var.memory_size
  enable_vpc                     = true
  vpc_id                         = var.vpc_id
  private_subnet_ids             = var.private_subnet_ids
  sync_image                     = true
  sync_source_repo               = "champtitles/terraform-aws-rabbitmq-lambda"
  ecr_name                       = "terraform-aws-rabbitmq-lambda-${random_id.this[0].hex}"
  ecr_tag                        = module.hash.hash
  reserved_concurrent_executions = var.reserved_concurrent_executions
  environment = {
    RABBITMQ_HOST         = var.rabbitmq_host
    RABBITMQ_PORT         = var.rabbitmq_port
    RABBITMQ_USER         = var.rabbitmq_user
    RABBITMQ_PASSWORD_SSM = var.rabbitmq_password_ssm
  }
}
