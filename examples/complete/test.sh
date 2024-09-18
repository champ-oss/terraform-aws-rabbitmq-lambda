set -e

aws lambda invoke \
    --cli-binary-format raw-in-base64-out \
    --function-name $FUNCTION_NAME \
    --cli-binary-format raw-in-base64-out \
    --payload '{"exchange":"","routing_key":"test","body":"test"}' \
    response.json

cat response.json