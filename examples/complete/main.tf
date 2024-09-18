locals {
  git = "terraform-aws-rabbitmq-lambda"
}

data "aws_vpcs" "this" {
  tags = {
    purpose = "vega"
  }
}

data "aws_subnets" "this" {
  tags = {
    purpose = "vega"
    Type    = "Private"
  }

  filter {
    name   = "vpc-id"
    values = [data.aws_vpcs.this.ids[0]]
  }
}

resource "aws_security_group" "rabbit" {
  name_prefix = "test-mq-"
  vpc_id      = data.aws_vpcs.this.ids[0]
}

module "rabbit" {
  source                   = "github.com/champ-oss/terraform-aws-mq.git?ref=v1.0.65-8ede199"
  git                      = local.git
  vpc_id                   = data.aws_vpcs.this.ids[0]
  source_security_group_id = aws_security_group.rabbit.id
  subnet_ids               = [data.aws_subnets.this.ids[0]]
  deployment_mode          = "SINGLE_INSTANCE"
  host_instance_type       = "mq.t3.micro"
  storage_type             = null
  cidr_allow_list          = ["10.0.0.0/8"]
  use_aws_owned_key        = true
  apply_immediately        = true
  engine_version           = "3.12.13"
}

module "this" {
  source                = "../../"
  git                   = local.git
  private_subnet_ids    = data.aws_subnets.this.ids
  vpc_id                = data.aws_vpcs.this.ids[0]
  rabbitmq_host         = module.rabbit.broker_host
  rabbitmq_password_ssm = module.rabbit.password_ssm_name
}

output "function_name" {
  description = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function#function_name"
  value       = module.this.function_name
}