import os
import ssl

import boto3

import pika
from pika.channel import Channel

HOST: str = os.environ.get('RABBITMQ_HOST', 'localhost')
PORT: int = int(os.environ.get('RABBITMQ_PORT', '5672'))
USER: str = os.environ.get('RABBITMQ_USER', 'guest')
PASSWORD: str = os.environ.get('RABBITMQ_PASSWORD', 'guest')
PASSWORD_SSM: str = os.environ.get('RABBITMQ_PASSWORD_SSM')
SSL_OPTIONS = pika.SSLOptions(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SSM_CLIENT = boto3.client('ssm', region_name=AWS_REGION)


def handler(event: dict, __) -> str:
    exchange = event.get('exchange', '')
    routing_key = event.get('routing_key')
    body = event.get('body')
    if not routing_key or not body:
        return 'body and routing_key is required'

    print(f'publishing message: exchange:"{exchange}" routing key:"{routing_key}"')
    channel = _get_channel()
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=body)


def _get_channel() -> Channel:
    print(f'Connecting to RabbitMQ host: {HOST}:{PORT}')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=HOST,
        port=PORT,
        credentials=pika.PlainCredentials(USER, _get_password()),
        ssl_options=SSL_OPTIONS if PORT == 5671 else None
    ))
    return connection.channel()


def _get_password() -> str:
    if not PASSWORD_SSM:
        return PASSWORD
    print(f'loading password from SSM parameter:{PASSWORD_SSM}')
    response = SSM_CLIENT.get_parameter(Name=PASSWORD_SSM, WithDecryption=True)
    return response.get('Parameter', {}).get('Value')


if __name__ == '__main__':
    handler({
        'routing_key': 'test-queue',
        'body': 'Hello World!',
    }, None)
