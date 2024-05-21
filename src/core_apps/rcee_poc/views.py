# views.py

import docker
from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured

from rest_framework.views import APIView

# from .models import CodeSubmission
import tempfile
import uuid
import os, json, time, random


from core_apps.rcee_poc.file_data_processor import file_processor
from core_apps.rcee_poc.container import code_container
from core_apps.rcee_poc.exec_engine import code_exec_engine


try:
    from docker import from_env
except ImportError:
    raise ImproperlyConfigured("Docker library not installed. Please install 'docker'")


class CodeSubmitSimpleImplementation(APIView):
    """A simple approach to test the code submission without creating the files beforehand.
    In this use case, the host volume creation also handled by docker.
    The volume created in host by docker has permission only of docker, hence the files can not be deleted by host user.

    The time is also same as the robust implementation of creating files beforehand. Infact, this method takes one second more
    one average than the robust implementation.

    """

    def post(self, request):
        start = time.time()

        lang = request.data.get("lang")
        code = request.data.get("code")
        input_data = request.data.get("input")

        print("Code: ", code)

        client = from_env()

        file_path = f"user-files/{random.randint(10, 100000)}"
        curr_path = os.getcwd()
        print("curr path: ", os.getcwd())
        new_file_path = os.path.join(curr_path, file_path)

        try:
            # Create and start a container
            container = client.containers.run(
                "simple_cpp",  # Image name
                volumes={
                    f"{new_file_path}/": {
                        "bind": "/user-files",
                        "mode": "rw",
                    }
                },
                command=[
                    "sh",
                    "-c",
                    f'echo "{code}" > /user-files/code.cpp && echo "{input_data}" > /user-files/input.txt && g++ /user-files/code.cpp -o /user-files/code && /user-files/code < /user-files/input.txt > /user-files/output.txt',
                ],
                detach=True,
            )

            # Wait for the container to finish
            result = container.wait()
            print("result: ", result)

            # Get the logs (output)
            output = container.logs().decode("utf-8")

            with open(f"{new_file_path}/output.txt", "r") as f:
                data = f.read()
                print("data: ", data)

            # Remove the container
            container.remove()

            end = time.time()

            print("total time taken: ", end - start)
            # Return output to the user
            return JsonResponse({"output": output})

        except docker.errors.ContainerError as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)

        # return JsonResponse({"error": "Method not allowed"}, status=405)


class CodeSubmitRobustAPI(APIView):
    """An API to test the robust implementation of the Online Judge.
    
    and compare the time with simple implementation 
    """

    def post(self, request): 
        '''Submit code to execute in secure docker container.'''

        lang = request.data.get('lang')
        code = request.data.get('code')
        input_file = request.data.get('input')
        testcases = request.data.get('testcases')

        # print('lang: ', lang)
        # print("code: ", code)
        # print("input file ", input_file)
        # print("testcases: ", testcases)
        
        # print('request.data: ', request.data)
        # print('\ntype of requst.data: ', type(request.data))
        
        # print('\ntype of code: ', type(code))
        # print('\ntype of input: ', type(input_file))
        
        submission_id = uuid.uuid4()
        data = code_exec_engine(user_codes=request.data, submission_id=submission_id)
        
        return JsonResponse({'submission_id': submission_id, "data": data}, status=200)