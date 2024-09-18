import os
import ssl
from importlib import reload
from unittest import TestCase
from unittest.mock import patch

from pika.connection import ConnectionParameters, SSLOptions
from pika.credentials import PlainCredentials


class Test(TestCase):

    test_event = {
        'routing_key': 'test-routing',
        'exchange': 'test-exchange',
        'body': 'test-body'
    }

    @patch('main.boto3.client')
    @patch('main.pika.BlockingConnection')
    def test_handler_for_localhost(self, mock_pika_blocking_connection, boto3_client):
        os.environ.clear()
        import main
        reload(main)
        main.handler(self.test_event, None)

        mock_pika_blocking_connection.assert_called_with(
            ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=PlainCredentials('guest', 'guest'),
                ssl_options=None)
        )

        mock_pika_blocking_connection.return_value.channel.return_value.basic_publish.assert_called_with(
            exchange='test-exchange',
            routing_key='test-routing',
            body='test-body')

    @patch('main.boto3.client')
    @patch('main.pika.BlockingConnection')
    def test_handler_with_ssl_enabled(self, mock_pika_blocking_connection, boto3_client):
        os.environ.clear()
        os.environ['RABBITMQ_PORT'] = '5671'
        import main
        reload(main)
        main.handler(self.test_event, None)

        mock_pika_blocking_connection.assert_called_with(
            ConnectionParameters(
                host='localhost',
                port=5671,
                credentials=PlainCredentials('guest', 'guest'),
                ssl_options=SSLOptions(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)))
        )

    @patch('main.boto3.client')
    @patch('main.pika.BlockingConnection')
    def test_handler_with_missing_values(self, mock_pika_blocking_connection, boto3_client):
        os.environ.clear()
        os.environ['RABBITMQ_PORT'] = '5671'
        import main
        reload(main)
        result = main.handler({}, None)
        assert result == 'body and routing_key is required'

    @patch('main.boto3.client')
    @patch('main.pika.BlockingConnection')
    def test_handler_with_ssm_password(self, mock_pika_blocking_connection, boto3_client):
        os.environ.clear()
        os.environ['RABBITMQ_PASSWORD_SSM'] = 'test-ssm'
        import main
        reload(main)
        main.handler(self.test_event, None)
        boto3_client.return_value.get_parameter.assert_called_with(Name='test-ssm', WithDecryption=True)
