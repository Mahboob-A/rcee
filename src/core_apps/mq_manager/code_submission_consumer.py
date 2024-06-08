# python
import logging
from typing import Callable

# pika
import pika

# django
from django.conf import settings

logger = logging.getLogger(__name__)


class CloudAMQPHandler:
    """CloudAMQP Handler Class to Declare Exchange and Queue
    for Code Submission Consumption [Published by Code Manager Service]
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
            exchange=settings.CPP_CODE_SUBMISSION_EXCHANGE_NAME,
            exchange_type=settings.CPP_CODE_SUBMISSION_EXCHANGE_TYPE,
        )
        # declare queue
        self.channel.queue_declare(queue=settings.CPP_CODE_SUBMISSION_QUEUE_NAME)
        # binding exchange and queue
        self.channel.queue_bind(
            settings.CPP_CODE_SUBMISSION_QUEUE_NAME,
            settings.CPP_CODE_SUBMISSION_EXCHANGE_NAME,
            settings.CPP_CODE_SUBMISSION_BINDING_KEY,
        )


class CodeSubmissionConsumerMQ(CloudAMQPHandler):
    """Interface calss to Consume messages from
    Code Submission Queue [Published by Code Manager Service]
    """

    def consume_messages(self, callback: Callable) -> None:
        try:
            self.connect()
            self.prepare_exchange_and_queue()

            self.channel.basic_consume(
                settings.CPP_CODE_SUBMISSION_QUEUE_NAME, callback, auto_ack=True
            )

            logger.info(
                f"\n\n[MQ Code Submission Consumer BEGIN]: Message Consumption from Code Submisison Queue Started."
            )
            self.channel.start_consuming()
            logger.info(
                f"\n\n[MQ Code Submission Consume SUCCESS]: Message Consuming Finished from Code Submission Queue."
            )
        except Exception as e:
            logger.exception(
                f"\n\n[MQ Code Submission Consumer EXCEPTION]: Exception Occurred During Cnsuming Messages from Code Submission MQ\n[EXCEPTION]: {str(e)}\n"
            )


code_submission_consumer_mq = CodeSubmissionConsumerMQ()
