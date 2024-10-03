output "arn" {
  description = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function#arn"
  value       = var.enabled ? module.this.arn : ""
}

output "aws_region" {
  description = "AWS region name"
  value       = var.enabled ? data.aws_region.this[0].name : ""
}

output "function_name" {
  description = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function#function_name"
  value       = var.enabled ? module.this.function_name : ""
}

output "private_subnet_ids" {
  description = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_subnet_group#subnet_ids"
  value       = var.enabled ? var.private_subnet_ids : []
}

output "vpc_id" {
  description = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group#vpc_id"
  value       = var.enabled ? var.vpc_id : ""
}