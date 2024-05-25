import json, traceback, logging

from django.conf import settings

from core_apps.code_consumer.mq_consumer import data_consumer
from core_apps.rce_engine.exec_engine import code_execution_engine

logger = logging.getLogger(__name__)


def callback(channel, method, properties, body):
    try:

        # body is in bytes. decodes to str then as dict
        data = json.loads(body.decode("utf-8"))

        processed_data = {
            "user_id": data["user_details"].get("user_id"),
            "submission_id": data.get("submission_id"),
            "lang": data.get("lang"),
            "inputs": data.get("inputs"),
            "testcases": data.get("testcases"),
            "code": data.get("code"),
        }
        
        # call the judge to execute the result.
        result = code_execution_engine.exec_code(
            user_codes=processed_data, submission_id=data.get("submission_id")
        )

        # call the publisher to publish the result.
        print("\n\nexe result: ", result)

    except Exception as e:
        logger.exception(
            f"[MQ Callback EXCEPTION]: Exception Occurred at Callback.\n[EXCEPTION]: {str(e)}"
        )
        print("\nTraceback Print")
        traceback.print_exc()


def main():
    logger.info(f"\n[In MAIN]: In main Func of Callback.")
    data_consumer.consume_messages(callback=callback)
