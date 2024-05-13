import json, traceback, logging

from django.conf import settings

from core_apps.code_consumer.mq_consumer import data_consumer

logger = logging.getLogger(__name__)


def callback(channel, method, properties, body):
    try:
        print("callback")
        print("body: ", body)
        print('body type: ', type(body))
        data = body.decode('utf-8')
        print('data: ', data)
        print('data type: ', type(data))

    except Exception as e:
        logger.exception(
            f"[MQ Callback EXCEPTION]: Exception Occurred at Callback.\n[EXCEPTION]: {str(e)}"
        )
        print("\nTraceback Print")
        traceback.print_exc()

def main(): 
    logger.info(f'\n[In MAIN]: In main Func of Callback.')
    data_consumer.consume_messages(callback=callback)
