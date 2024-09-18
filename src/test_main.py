import os
import ssl
from importlib import reload
from unittest import TestCase
from unittest.mock import patch

from pika.connection import ConnectionParameters, SSLOptions
from pika.credentials import PlainCredentials
from src import main


class Test(TestCase):

    test_event = {
        'queue': 'test-queue',
        'routing_key': 'test-routing',
        'exchange': 'test-exchange',
        'body': 'test-body'
    }

    @patch('main.pika.BlockingConnection')
    def test_handler_for_localhost(self, mock_pika_blocking_connection):
        os.environ.clear()
        reload(main)
        main.handler(self.test_event, None)

        mock_pika_blocking_connection.assert_called_with(
            ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=PlainCredentials('guest', 'guest'),
                ssl_options=None)
        )

        mock_pika_blocking_connection.return_value.channel.return_value.queue_declare.assert_called_with(
            queue='test-queue')

        mock_pika_blocking_connection.return_value.channel.return_value.basic_publish.assert_called_with(
            exchange='test-exchange',
            routing_key='test-routing',
            body='test-body')

    @patch('main.pika.BlockingConnection')
    def test_handler_with_ssl_enabled(self, mock_pika_blocking_connection):
        os.environ['RABBITMQ_PORT'] = '5671'
        reload(main)
        main.handler({'queue': 'test-queue'}, None)

        mock_pika_blocking_connection.assert_called_with(
            ConnectionParameters(
                host='localhost',
                port=5671,
                credentials=PlainCredentials('guest', 'guest'),
                ssl_options=SSLOptions(context=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)))
        )
