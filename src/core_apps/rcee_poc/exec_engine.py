# exec_engine.py | run rce engine locally without http request from here.

import docker
from django.http import JsonResponse

# from .models import CodeSubmission
import tempfile
import uuid
import os, json, time

from core_apps.rcee_poc.file_data_processor import file_processor
from core_apps.rcee_poc.container import code_container
from core_apps.rcee_poc.compare_testcases import compare_output_and_testcases



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


######################################################################
# Entrypoint function.
######################################################################

from core_apps.rcee_poc.questions import (
    hello_world_with_num_data_problem,
    sum_of_a_b_problem,
    time_limit_exceed_problem,
    memory_limit_exceed_problem,
)


def test_code_exec():

    start_time = time.time()

    # write the user codes in file system
    result = file_processor.write_data(data=sum_of_a_b_problem)  # pass the code here.

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
        print("File Write Message: ", file_write_message)
        print("\n")

        # code_filepath:  base-dir/user_codes/lang/uuid/main.cpp
        # parent_dir:  base-dir/user_codes/lang/uuid
        parent_dir = os.path.dirname(code_filepath)

        # create the container
        container_error_message, data = code_container.run_container(
            user_file_parent_dir=parent_dir
        )

        status_code = data.get("status_code")
        status = data.get("status")
        error_message = data.get("error_message")
        success_message = data.get("success_message")

        # return the data.
        return_data = {}

        # no error in docker. now data dict contains data, else data is an empty dict.
        if container_error_message is None:
            # output is written in output.txt. check output.txt to compare with testcase.txt
            if status_code == 0:
                verdict = compare_output_and_testcases(
                    output_filepath=output_filepath, testcases_filepath=testcases_flepath
                )

                return_data = print_and_get_formatted_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                    verdict=verdict
                )
                return return_data

            else:  #  compilation error or other error. output.txt is empty.
                return_data = print_and_get_formatted_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                )
            end_time = time.time()
            print("\n\bViews.py time: ", end_time - start_time)
            return return_data
        else:  # some system and docker related error, TLE, Memory LImit etc.
            if data.get("status_code") == 124:
                return_data = print_and_get_formatted_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                )
                return return_data
            else:
                print(container_error_message)
                return container_error_message

    else:  # data write in file system is unsuccessfu.
        error_message = result[1]
        print("\nFile Write Error: ", error_message)
        return (f"File Write Error", error_message)

# import this func to test in api.
def code_exec_engine(user_codes: dict):
    """Main entrypont function to run code execution.

    Args:
        Dict: user codes, input.txt, testcases.txt

    Return:
        Dict: execution result
    """
    # write the user codes in file system
    result = file_processor.write_data(data=user_codes)  # pass the code here.

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
        print("File Write Message: ", file_write_message)
        print("\n")

        # code_filepath:  base-dir/user_codes/lang/uuid/main.cpp
        # parent_dir:  base-dir/user_codes/lang/uuid
        parent_dir = os.path.dirname(code_filepath)

        # create the container
        container_error_message, data = code_container.run_container(
            user_file_parent_dir=parent_dir
        )

        status_code = data.get("status_code")
        status = data.get("status")
        error_message = data.get("error_message")
        success_message = data.get("success_message")

        # return the data.
        return_data = {}

        # no error in docker. now data dict contains data, else data is an empty dict.
        if container_error_message is None:
            # output is written in output.txt. check output.txt to compare with testcase.txt
            if status_code == 0:
                verdict = compare_output_and_testcases(
                    output_filepath=output_filepath,
                    testcases_filepath=testcases_flepath,
                )

                return_data = print_and_get_formatted_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                    verdict=verdict,
                )
                return return_data

            else:  #  compilation error or other error. output.txt is empty.
                return_data = print_and_get_formatted_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                )
            return return_data
        else:  # some system and docker related error, TLE, Memory LImit etc.
            if data.get("status_code") == 124:
                return_data = print_and_get_formatted_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                )
                return return_data 
            else:
                # print(container_error_message)
                return container_error_message 

    else:  # data write in file system is unsuccessfu.
        error_message = result[1]
        print("\nFile Write Error: ", error_message)
        return (f"File Write Error", error_message)


if __name__ == "__main__":

    strt_time = time.time()
    test_code_exec()
    end_time = time.time()
    print("whole time: ", end_time - strt_time)
