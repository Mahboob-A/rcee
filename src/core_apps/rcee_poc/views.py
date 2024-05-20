# views.py

import docker
from django.http import JsonResponse

# from .models import CodeSubmission
import tempfile
import uuid
import os, json, time

from file_data_processor import file_processor
from container import code_container


def execute_code(request):
    if request.method == "POST":
        # Get JSON data from the request
        # data = request.POST.get(
        #     "data"
        # )  # Assuming JSON data is sent in the request body

        # Parse JSON data
        lang = request.POST.get("lang")
        code = request.POST.get("code")

        # flow 01: create a submission id. it will be the only identifier for the user code.
        # submission_id =

        # Save code submission to database
        # submission = CodeSubmission.objects.create(lang=lang, code=code)

        # Execute code in a Docker container
        client = docker.from_env()
        container = client.containers.run(
            "cpp_image",
            command=[
                "sh",
                "-c",
                f'echo "{code}" > code.cpp && g++ code.cpp -o code && ./code',
            ],
        )

        # Capture output
        output = container.decode("utf-8")

        # Return output to the user
        return JsonResponse({"output": output})

    return JsonResponse({"error": "Method not allowed"}, status=405)


def format_error_message(error_message: str, status_code=None):
    """Format the error message to return to the user.

          Only return the main.cpp: part.

          example error message:
    /user-codes/cpp/result/main.cpp: In function 'int main()':
    /user-codes/cpp/result/main.cpp:17:9: error: 'sol' was not declared in this scope; did you mean 'solp'?
       17 |         sol(num);
          |         ^~~
          |         solp
    """
    if status_code == 137: 
        return "Memory Limit Exceed"
    elif status_code == 124: 
        return "Time Limit Exceed"
    elif status_code == 139: 
        return "Index Out Of Bound"
    elif status_code == 1: 
        error_message = error_message.split("/")
        return error_message[8]
    else: 
        # other g++ compilation error
        return error_message 


def compare_test_cases(output_filepath: str, testcases_filepath: str):
    output_content = ""
    testcases_content = ""

    with open(output_filepath, "r") as output_file:
        output_content = output_file.read().strip()

    with open(testcases_filepath, "r") as testcases_file:
        testcases_content = testcases_file.read().strip()

    print("\n[X]: output file content: \n", output_content)
    print("\n[X]: testcases file content: \n", testcases_content)

    if output_content == testcases_content:
        print("\nresult: Accepted")
    else:
        print("\nresult: Wrong Answer")


def print_messages(
    status_code: int, status: str, success_message: str, error_message: str
):
    print("status_code: ", status_code)
    print("status: ", status)
    print("error message: ", error_message)
    print("success message: ", success_message)


######################################################################
# Entrypoint function.
######################################################################

from questions import (
    hello_world_with_num_data_problem, 
    sum_of_a_b_problem, 
    time_limit_exceed_problem, 
    memory_limit_exceed_problem
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

        # no error in docker. now data dict contains data, else data is an empty dict.
        if container_error_message is None:
            # output is written in output.txt. check output.txt to compare with testcase.txt
            if status_code == 0:
                result = compare_test_cases(output_filepath, testcases_flepath)
                print_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                )
            else:  #  compilation error or other error. output.txt is empty.
                formatted_error_message = format_error_message(
                    error_message=error_message, status_code=status_code
                )
                print_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=formatted_error_message,
                )
            end_time = time.time()
            print("\n\bViews.py time: ", end_time - start_time)
        else:  # some system and docker related error, TLE, Memory LImit etc.
            if data.get("status_code") == 124:
                print_messages(
                    status_code=status_code,
                    status=status,
                    success_message=success_message,
                    error_message=error_message,
                )
            else:
                print(container_error_message)
    else:  # data write in file system is unsuccessfu.
        error_message = result[1]
        print("\nFile Write Error: ", error_message)


strt_time = time.time()
test_code_exec()
end_time = time.time()
print("whole time: ", end_time - strt_time)
