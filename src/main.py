import os
import logging
import pika
import ssl
import boto3

logging.basicConfig(level=logging.INFO)

HOST: str = os.environ.get('RABBITMQ_HOST', 'localhost')
PORT: int = int(os.environ.get('RABBITMQ_PORT', '5672'))
USER: str = os.environ.get('RABBITMQ_USER', 'guest')
PASSWORD: str = os.environ.get('RABBITMQ_PASSWORD', 'guest')
PASSWORD_SSM: str = os.environ.get('RABBITMQ_PASSWORD_SSM')
SSL_OPTIONS = pika.SSLOptions(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
PARAMS = pika.ConnectionParameters(
    host=HOST,
    port=PORT,
    credentials=pika.PlainCredentials(USER, PASSWORD),
    ssl_options=SSL_OPTIONS if PORT == 5671 else None
)
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SSM_CLIENT = boto3.client('ssm', region_name=AWS_REGION)


def handler(event: dict, __) -> str:
    # if PASSWORD_SSM:
    #     response = SSM_CLIENT.get_parameter(Name=PASSWORD_SSM,WithDecryption=True)
    #     password = response.get('Parameter', {}).get('Value')

    exchange = event.get('exchange', '')
    routing_key = event.get('routing_key')
    body = event.get('body')
    if not routing_key or not body:
        return 'body and routing_key is required'

    logging.info('Connecting to RabbitMQ host: %s:%s', HOST, PORT)
    connection = pika.BlockingConnection(PARAMS)
    channel = connection.channel()

    logging.info('publishing message: exchange:"%s" routing key:"%s"', exchange, routing_key)
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=body
    )


if __name__ == '__main__':
    handler({
        'routing_key': 'test-queue',
        'body': 'Hello World!',
    }, None)
