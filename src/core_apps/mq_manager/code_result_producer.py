# python
import os, json, logging

# django
from django.conf import settings

# pika
import pika

logger = logging.getLogger(__name__)


class CloudAMQPHandler:
    """CloudAMQP Handler Class to Declare Exchange and Queue
    for Code Result Publication
    """

    def __init__(self) -> None:
        self.broker_url = settings.CLOUD_AMQP_URL
        self.params = pika.URLParameters(self.broker_url)

    def connect(self):
        self.__connection = pika.BlockingConnection(parameters=self.params)
        self.channel = self.__connection.channel()

    def prepare_exchange_and_queue(self) -> None:
        # exchange declare
        self.channel.exchange_declare(
            exchange=settings.RESULT_PUBLISH_EXCHANGE_NAME,
            exchange_type=settings.RESULT_PUBLISH_EXCHANGE_TYPE,
        )
        # declare queue
        self.channel.queue_declare(queue=settings.RESULT_PUBLISH_QUEUE_NAME)
        # binding exchange and queue
        self.channel.queue_bind(
            settings.RESULT_PUBLISH_QUEUE_NAME,
            settings.RESULT_PUBLISH_EXCHANGE_NAME,
            settings.RESULT_PUBLISH_BINDING_KEY,
        )


class CodeEXECResultPublisherMQ(CloudAMQPHandler):
    """Interface class to publish data to MQ
    Publish Code Execution Result to Result Queue
    """

    def publish_data(self, result_data: json, username: str) -> None:
        # connect to mq and prepare exchange and queue

        try:
            self.connect()
            self.prepare_exchange_and_queue()
            self.channel.basic_publish(
                exchange=settings.RESULT_PUBLISH_EXCHANGE_NAME,
                routing_key=settings.RESULT_PUBLISH_ROUTING_KEY,
                body=result_data,
            )
            logger.info(
                f"\n[MQ SUCCESS]: Code Execution Result for UN: '{username}' Successfully Published to Result MQ."
            )
            message = "success"
            return True, message
        except Exception as e:
            logger.exception(
                f"\n[MQ ERROR]: Code Execution Result for UN: '{username}' Could not be published to Result MQ.\n[MQ EXCEPTION]: {str(e)}"
            )
            message = "error-publishing-to-code-exececution-result-mq"
            return False, message


# instance to call
result_producer_mq = CodeEXECResultPublisherMQ()
