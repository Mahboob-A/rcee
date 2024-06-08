import json
import logging
import traceback

# MQ Code Execution Result Publish
from core_apps.mq_manager.code_result_producer import result_producer_mq

# MQ Code Submission Consume
from core_apps.mq_manager.code_submission_consumer import code_submission_consumer_mq

# RCE Engine
from core_apps.rce_engine.exec_engine import code_execution_engine

logger = logging.getLogger(__name__)


def callback(channel, method, properties, body):
    """The callback consumes from the Code Submission Queue
    Published by Code Manager Service.
    The callback consumes the message. The message contains user code, testcases, inputs etc.
    to run the RCE Engine and generate a result.

    The callback does the following:
    A. It consumes from the Code Submission Queue Published by the Code Manager Service.
        A1. Calls the RCE Engine to execute the code.

    B. Once the code execution result is received, the callback again calls Result Producer.
       B1. The Result Producer produces the code execution result to Code Execution Result Queue
             Which is consumed by Code Manager Service to save to DB and return the result to the User.
    """
    try:
        # body is in bytes. decodes to str then as dict
        data = json.loads(body.decode("utf-8"))

        processed_data = {
            "submission_id": data.get("submission_id"),
            "lang": data.get("lang"),
            "inputs": data.get("inputs"),
            "testcases": data.get("testcases"),
            "code": data.get("code"),
        }

        username = data["user_details"].get("username")

        # call the judge to execute the result.
        result_data = code_execution_engine.exec_code(
            user_codes=processed_data, submission_id=data.get("submission_id")
        )

        # put the user details and submission id in the final result.
        result_data["user_details"] = data["user_details"]
        result_data["submission_id"] = data.get("submission_id")

        logger.info(
            f"\n\n[Code EXEC Success]: Code Consume and Execution Successful for Username: {username}"
        )
        
        # Publish the result to the Result Queue as JSON
        result_data = json.dumps(result_data)
        result_producer_mq.publish_data(result_data=result_data, username=username)

    except Exception as e:
        logger.exception(
            f"\n\n[MQ Code Submision Consume ERROR]: Exception Occurred at Callback .\n[EXCEPTION]: {str(e)}"
        )
        logger.error("\nTraceback")
        traceback.print_exc()


def main():
    logger.info(f"\n\n[In MAIN]: In main Func of Code Submission ConsumeCallback .")
    code_submission_consumer_mq.consume_messages(callback=callback)
