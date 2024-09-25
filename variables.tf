variable "enabled" {
  description = "Set to false to prevent the module from creating any resources"
  type        = bool
  default     = true
}

variable "git" {
  description = "Name of the Git repo"
  type        = string
}

variable "memory_size" {
  description = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function#memory_size"
  type        = number
  default     = 128
}

variable "private_subnet_ids" {
  description = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_subnet_group#subnet_ids"
  type        = list(string)
}

variable "reserved_concurrent_executions" {
  description = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function#reserved_concurrent_executions"
  type        = number
  default     = 1
}

variable "rabbitmq_host" {
  description = "RabbitMQ DNS hostname"
  type        = string
}

variable "rabbitmq_port" {
  description = "RabbitMQ port"
  type        = string
  default     = "5671"
}

variable "rabbitmq_user" {
  description = "RabbitMQ username"
  type        = string
  default     = "mqadminuser"
}

variable "rabbitmq_password_ssm" {
  description = "SSM parameter name containing the RabbitMQ password"
  type        = string
}

variable "runtime" {
  description = "https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html"
  type        = string
  default     = "python3.12"
}

variable "tags" {
  description = "Map of tags to assign to resources"
  type        = map(string)
  default     = {}
}

variable "vpc_id" {
  description = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group#vpc_id"
  type        = string
}