# python
import logging
from typing import Callable

# django
from django.conf import settings

# pika
import pika


logger = logging.getLogger(__name__)


class CloudAMQPHelper:
    """Helper class to connect with RabbitMQ Server"""

    def __init__(self) -> None:
        self.broker_url = settings.CLOUD_AMQP_URL
        self.params = pika.URLParameters(self.broker_url)

    def connect(self) -> None:
        self.__connection = pika.BlockingConnection(parameters=self.params)
        self.chanel = self.__connection.channel()

    def prepare_exchange_and_queue(self) -> None:
        # exchange declare
        self.chanel.exchange_declare(
            exchange=settings.EXCHANGE_NAME, exchange_type=settings.EXCHANGE_TYPE
        )

        # queue declare
        self.chanel.queue_declare(settings.QUEUE_NAME)

        # bind exchange and queue
        self.chanel.queue_bind(
            settings.QUEUE_NAME, settings.EXCHANGE_NAME, settings.BINDING_KEY
        )


class DataConsumerMQ(CloudAMQPHelper):
    """Interface calss to Consume messages from MQ"""

    def consume_messages(self, callback: Callable) -> None:
        try:
            self.connect()
            self.prepare_exchange_and_queue()

            self.chanel.basic_consume(settings.QUEUE_NAME, callback, auto_ack=True)

            logger.info(f"\n[MQ Consume BEGIN]: Message consuming started.")
            self.chanel.start_consuming()
            logger.info(f"\n[MQ Consume SUCCESS]: Message consuming finished.")
        except Exception as e:
            logger.exception(
                f"\n[MQ Consumer EXCEPTION]: Exception Occurred During Cnsuming Messages from MQ\n[EXCEPTION]: {str(e)}\n"
            )


data_consumer = DataConsumerMQ()