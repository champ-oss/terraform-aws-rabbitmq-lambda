"""Publishes a message to RabbitMQ."""
import os
import ssl

import boto3
import pika
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from pika.channel import Channel

logger: Logger = Logger()
HOST: str = os.environ.get('RABBITMQ_HOST', 'localhost')
PORT: int = int(os.environ.get('RABBITMQ_PORT', '5672'))
USER: str = os.environ.get('RABBITMQ_USER', 'guest')
PASSWORD: str = os.environ.get('RABBITMQ_PASSWORD', 'guest')
PASSWORD_SSM: str = os.environ.get('RABBITMQ_PASSWORD_SSM')
SSL_OPTIONS = pika.SSLOptions(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SSM_CLIENT = boto3.client('ssm', region_name=AWS_REGION)


@logger.inject_lambda_context(log_event=True)
def handler(event: dict, context: LambdaContext) -> str:
    """
    Handle the main execution of the script.

    :return: None
    """
    exchange = event.get('exchange', '')
    routing_key = event.get('routing_key')
    body = event.get('body')
    if not routing_key or not body:
        return 'body and routing_key is required'

    logger.info(f'publishing message: exchange:"{exchange}" routing key:"{routing_key}"')
    channel = _get_channel()
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)
    return 'Message published'


def _get_channel() -> Channel:
    logger.info(f'Connecting to RabbitMQ host: {HOST}:{PORT}')
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
    logger.info(f'loading password from SSM parameter:{PASSWORD_SSM}')
    response = SSM_CLIENT.get_parameter(Name=PASSWORD_SSM, WithDecryption=True)
    return response.get('Parameter', {}).get('Value')


if __name__ == '__main__':
    handler({'routing_key': 'test-queue', 'body': 'Hello World!'}, None)
