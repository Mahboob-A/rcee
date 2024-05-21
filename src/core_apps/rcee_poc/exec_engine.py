# exec_engine.py | run rce engine locally without http request from here.

import docker
from django.http import JsonResponse

# from .models import CodeSubmission
import tempfile
import uuid
import os, json, time, logging 

from core_apps.rcee_poc.file_data_processor import file_processor
from core_apps.rcee_poc.container import code_container
from core_apps.rcee_poc.compare_testcases import compare_output_and_testcases

# to test the RCE Engine Locally. 
from core_apps.rcee_poc.questions import (
    hello_world_with_num_data_problem,
    sum_of_a_b_problem,
    time_limit_exceed_problem,
    memory_limit_exceed_problem,
)


logger = logging.getLogger(__name__)


def print_and_get_formatted_messages(
    status_code: int, status: str, success_message: str, error_message: str, verdict: str=None 
):
    print("status_code: ", status_code)
    print("status: ", status)
    print("error message: ", error_message)
    print("success message: ", success_message)

    if verdict is not None: # verdict (AC or WA)
        data = {
            "result": verdict, 
            "status_code": status_code,
            "status": status,
            "error_message": error_message,
            "success_message": success_message,
        }
    else: 
        data = {
            "status_code": status_code,
            "status": status,
            "error_message": error_message,
            "success_message": success_message,
        }
    return data


def get_formatted_messages(
    status_code: int,
    status: str,
    success_message: str,
    error_message: str,
    verdict: str = None,
):

    if verdict is not None:  # verdict (AC or WA)
        data = {
            "result": verdict,
            "status_code": status_code,
            "status": status,
            "error_message": error_message,
            "success_message": success_message,
        }
    else:
        data = {
            "status_code": status_code,
            "status": status,
            "error_message": error_message,
            "success_message": success_message,
        }
    return data


# import this func to test in api.
def code_exec_engine(user_codes: dict, submission_id: str):
    """Main entrypont function to run code execution.

    Args:
        Dict: user codes, input.txt, testcases.txt
        Str: submission_id for the user code submission

    Return:
        Dict: 
            Execution Result:
                data:{status_code, status, success_message, error_message, {data:None{result: result, verdict}}  
    """
    # write the user codes in file system
    result = file_processor.write_data(data=user_codes, submission_id=submission_id)  # pass and submission the code here.

    write_success = result[0]

    # data write in filesystem is successful.
    if write_success is not None:
        (
            code_filepath,
            input_filepath,
            output_filepath,
            testcases_flepath,
            file_write_message,
        ) = result[1:]

        # code_filepath:  base-dir/user_codes/lang/uuid/main.cpp
        # parent_dir:  base-dir/user_codes/lang/uuid
        parent_dir = os.path.dirname(code_filepath)

        # create the container, run the user code, compare the testcases, and get the result dict.
        container_error_message, data = code_container.run_container(
            user_file_parent_dir=parent_dir, submission_id=submission_id
        )

        status_code = data.get("status_code")
        status = data.get("status")
        error_message = data.get("error_message")
        success_message = data.get("success_message")

        # return the data.
        return_data = {}

        # no error in docker. now data dict contains data related to code result, else data is an empty dict.
        if container_error_message is None:
            # output is written in output.txt. check output.txt to compare with testcase.txt
            if status_code == 0:
                verdict = compare_output_and_testcases(
                    output_filepath=output_filepath,
                    testcases_filepath=testcases_flepath,
                )
                return_data = get_formatted_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                    verdict=verdict,
                )
            else:  #  compilation error or other error. output.txt is empty.
                return_data = get_formatted_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                )

        # some system and docker related error, TLE, Memory LImit etc.
        else:  
            if data.get("status_code") == 124:
                return_data = get_formatted_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                )
            else:
                #  Delete the created files.
                file_processor.del_user_dirs_files(
                    filepath=parent_dir, submission_id=submission_id
                )
                return container_error_message 

        #  Delete the created files before returning the result. pass any filepath to delete all the files along with the unique uuid user dir.
        file_processor.del_user_dirs_files(
            filepath=code_filepath, submission_id=submission_id
        )
        return return_data

    else:  # data write in file system is unsuccessfu.
        error_message = result[1]
        logger.exception(f"\n\nFile Write Error: {error_message}")
        return (f"File Write Error: {error_message}")


if __name__ == "__main__":
    pass 
