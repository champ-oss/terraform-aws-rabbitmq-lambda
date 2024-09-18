set -e

aws lambda invoke --function-name $FUNCTION_NAME --payload '{"key1":"value1", "key2":"value2", "key3":"value3"}' response.json

cat response.json