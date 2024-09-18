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
SSL_OPTIONS = pika.SSLOptions(context=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT))
PARAMS = pika.ConnectionParameters(
    host=HOST,
    port=PORT,
    credentials=pika.PlainCredentials(USER, PASSWORD),
    ssl_options=SSL_OPTIONS if PORT == 5671 else None
)
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SSM_CLIENT = boto3.client('ssm', region_name=AWS_REGION)


def handler(event: dict, __) -> None:
    # if PASSWORD_SSM:
    #     response = SSM_CLIENT.get_parameter(Name=PASSWORD_SSM,WithDecryption=True)
    #     password = response.get('Parameter', {}).get('Value')

    queue = event.get('queue')
    routing_key = event.get('routing_key')
    exchange = event.get('exchange')
    body = event.get('body')

    logging.info("Connecting to RabbitMQ host: %s:%s", HOST, PORT)
    connection = pika.BlockingConnection(PARAMS)
    channel = connection.channel()

    if queue:
        logging.info("creating queue if not exists: %s", queue)
        channel.queue_declare(queue=queue)

    logging.info("publishing message to %s", queue)
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=body
    )


if __name__ == '__main__':
    handler({
        'queue': 'test-queue'
    }, None)
