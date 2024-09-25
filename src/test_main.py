"""Provide tests for main script."""
import os
import ssl
from importlib import reload
from typing_extensions import Self
from unittest import TestCase
from unittest.mock import patch, Mock

from pika.connection import ConnectionParameters, SSLOptions
from pika.credentials import PlainCredentials


class Test(TestCase):
    """Provide tests for main script."""

    test_event = {
        'routing_key': 'test-routing',
        'exchange': 'test-exchange',
        'body': 'test-body'
    }
    mock_context = Mock()

    @patch('main.boto3.client')
    @patch('main.pika.BlockingConnection')
    def test_handler_for_localhost(self: Self, mock_pika_blocking_connection: Mock, boto3_client: Mock) -> None:
        """Test handler function."""
        os.environ.clear()
        import main
        reload(main)
        main.handler(self.test_event, self.mock_context)

        mock_pika_blocking_connection.assert_called_with(
            ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=PlainCredentials('guest', 'guest'),
                ssl_options=None
            )
        )

        mock_pika_blocking_connection.return_value.channel.return_value.basic_publish.assert_called_with(
            exchange='test-exchange',
            routing_key='test-routing',
            body='test-body'
        )

    @patch('main.boto3.client')
    @patch('main.pika.BlockingConnection')
    def test_handler_with_ssl_enabled(self: Self, mock_pika_blocking_connection: Mock, boto3_client: Mock) -> None:
        """Test handler function with SSL enabled."""
        os.environ.clear()
        os.environ['RABBITMQ_PORT'] = '5671'
        import main
        reload(main)
        main.handler(self.test_event, self.mock_context)

        mock_pika_blocking_connection.assert_called_with(
            ConnectionParameters(
                host='localhost',
                port=5671,
                credentials=PlainCredentials('guest', 'guest'),
                ssl_options=SSLOptions(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
            )
        )

    @patch('main.boto3.client')
    @patch('main.pika.BlockingConnection')
    def test_handler_with_missing_values(self: Self, mock_pika_blocking_connection: Mock, boto3_client: Mock) -> None:
        """Test handler function when required payload values are missing."""
        os.environ.clear()
        os.environ['RABBITMQ_PORT'] = '5671'
        import main
        reload(main)
        result = main.handler({}, self.mock_context)
        assert result == 'body and routing_key is required'

    @patch('main.boto3.client')
    @patch('main.pika.BlockingConnection')
    def test_handler_with_ssm_password(self: Self, mock_pika_blocking_connection: Mock, boto3_client: Mock) -> None:
        """Test handler function with password loaded from SSM."""
        os.environ.clear()
        os.environ['RABBITMQ_PASSWORD_SSM'] = 'test-ssm'
        import main
        reload(main)
        main.handler(self.test_event, self.mock_context)
        boto3_client.return_value.get_parameter.assert_called_with(Name='test-ssm', WithDecryption=True)
