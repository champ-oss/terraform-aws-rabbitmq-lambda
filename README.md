# terraform-aws-rabbitmq-lambda
This is a Terraform module that creates an AWS Lambda function which can publish messages to RabbitMQ.

## Usage
See the [examples](./examples) directory for example usage.

Once the module is deployed, the Lambda function can be invoked with a payload like this:
```json
{
  "exchange": "my-exchange",
  "routing_key": "my-routing-key",
  "body": "Hello, World!"
}
```

You can also test the Lambda function using the AWS CLI with the command:
```bash
aws lambda invoke \
    --cli-binary-format raw-in-base64-out \
    --function-name my-function \
    --cli-binary-format raw-in-base64-out \
    --payload '{"exchange":"","routing_key":"test","body":"test"}' \
    response.json
```

<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

No providers.

## Modules

No modules.

## Resources

No resources.

## Inputs

No inputs.

## Outputs

No outputs.
<!-- END_TF_DOCS -->