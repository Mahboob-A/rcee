# views.py

import uuid

from django.http import JsonResponse

from rest_framework.views import APIView


# object to execute code metaclass=SignletonMeta
from core_apps.rce_engine.exec_engine import code_execution_engine


class CodeSubmitAPI(APIView):
    """An API to test the  implementation of the Online Judge.

        For testing: Currently returns the answer to the client. 
    """

    def post(self, request):
        """Submit code to execute in secure docker container."""

        lang = request.data.get("lang")
        code = request.data.get("code")
        input_file = request.data.get("input")
        testcases = request.data.get("testcases")

        print('request.data: ', request.data)
        print('request.data type: ', type(request.data))
        submission_id = uuid.uuid4()
        data = code_execution_engine.exec_code(
            user_codes=request.data, submission_id=submission_id
        )

        return JsonResponse({"submission_id": submission_id, "data": data}, status=200)
