# views.py

import docker
from django.http import JsonResponse

# from .models import CodeSubmission
import tempfile
import uuid
import os, json

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


two_sum_data = {
    "lang": "cpp",
    "code": '#include <iostream>\n#include <vector>\n#include <unordered_map>\nusing namespace std;\n\n\nvector<int> twoSum(vector<int>& nums, int target) {\n    unordered_map<int, int> num_map;\n    for (int i = 0; i < nums.size(); i++) {\n        int complement = target - nums[i];\n        if (num_map.find(complement) != num_map.end()) {\n            return {num_map[complement], i};\n        }\n        num_map[nums[i]] = i;\n    }\n    return {}; \n}\n\nint main() {\n    int t;\n    cin >> t; \n\n    for (int i = 0; i < t; i++) {\n        int n, target;\n        cin >> n >> target; \n\n        vector<int> nums(n);\n        for (int j = 0; j < n; j++) {\n            cin >> nums[j]; \n        }\n\n        vector<int> result = twoSum(nums, target);\n        if (!result.empty()) {\n            cout << result[0] << " " << result[1] << endl;\n        }\n    }\n\n    return 0;\n}\n',
    "input": [
        "10",
        "4 9",
        "2 7 11 15",
        "3 6",
        "3 2 4",
        "5 10",
        "8 1 5 3 7",
        "2 6",
        "1 4",
        "4 3",
        "2 1 4 7",
        "3 5",
        "5 2 8",
        "6 11",
        "6 5 3 9 4 2",
        "2 7",
        "3 5",
        "4 8",
        "7 1 6 4 9",
        "3 9",
        "1 3 5",
    ],
    "testcases": [
        "0 1",
        "1 2",
        "0 2",
        "2 4",
        "1 3",
        "0 1",
        "0 2",
        "2 3",
        "0 1",
        "1 2",
    ],
}

sum_of_a_b = {
    "lang": "cpp",
    "code": "#include <bits/stdc++.h>\nusing namespace std; \n\nvoid sum_of_a_b(int a, int b)\n{\n    cout << a + b << endl; \n}\n\n\nint main()\n{\n    int t, a, b; \n    cin >> t; \n    \n    while(t--)\n    {\n        cin >> a >> b; \n        sum_of_a_b(a, b); \n    }\n\n    return 0;\n}",
    "input": [
        "10", 
        "1 2", 
        "5 7",
        "4 6", 
        "10 5", 
        "15 15", 
        "25 30", 
        "150 50", 
        "100 200", 
        "110 90", 
        "1000 2000" 
    ],
    "testcases": [
        "3", 
        "12", 
        "10", 
        "15", 
        "30", 
        "55", 
        "200", 
        "300", 
        "200", 
        "300"
    ],
}


hello_world_with_num_data = {
    "lang": "cpp",
    "code": '#include <bits/stdc++.h>\nusing namespace std;\n\nvoid sol(int num)\n{\n    cout<<"Hello World: "<<num<<endl;\n}\n\nint main()\n{\n    int t, num; \n    cin>>t;\n\n    while(t--)\n    {\n        cin>>num; \n        sol(num);\n    }\n\n    return 0;\n}',
    "input": ["10", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    "testcases": [
        "Hello World: 1",
        "Hello World: 2",
        "Hello World: 3",
        "Hello World: 4",
        "Hello World: 5",
        "Hello World: 6",
        "Hello World: 7",
        "Hello World: 8",
        "Hello World: 9",
        "Hello World: 11",
    ],
}


def make_code_json():
    code = """#include <bits/stdc++.h>
using namespace std; 

int main()
{
    int arr[5] = {1, 2, 3}; 
    cout<<arr[0]<<endl; 
    cout<<arr[400]<<endl; 
    cout<<arr[6]<<endl; 
    
    return 0;
}
    """
    return code


def make_code_dict():
    code = make_code_json()
    data = {
        "lang": "cpp",
        "code": code,
        "input": ["10", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    }
    return data


def format_error_message(error_message: str): 
    """Format the error message to return to the user.

          Only return the main.cpp: part.

          example error message:
    /user-codes/cpp/result/main.cpp: In function 'int main()':
    /user-codes/cpp/result/main.cpp:17:9: error: 'sol' was not declared in this scope; did you mean 'solp'?
       17 |         sol(num);
          |         ^~~
          |         solp
    """
    error_message = error_message.split("/")
    return error_message[8]


def compare_test_cases(output_filepath: str, testcases_filepath: str): 
    output_content = ''
    testcases_content = ''

    with open(output_filepath, 'r') as output_file:
        output_content = output_file.read().strip()

    with open(testcases_filepath, "r") as testcases_file:
        testcases_content = testcases_file.read().strip()

    print("\n[X]: output file content: \n", output_content)
    print("\n[X]: testcases file content: \n", testcases_content)

    if output_content == testcases_content:
        print('\n[Success]: Accepted')
    else: 
        print('\n[Error]: Wrong Answer')


def test_code_exec():

    # write the user codes in file system
    data = make_code_dict()
    result = file_processor.write_data(data=hello_world_with_num_data)

    write_success = result[0]

    # data write in filesystem is successful.
    if write_success is not None:
        code_filepath, input_filepath, output_filepath, testcases_flepath, file_write_message = result[1:]
        print("\nCode File Path: ", code_filepath)
        print("File Write Message: ", file_write_message)
        print('\n\n')
        # code_filepath:  base-dir/user_codes/lang/uuid/main.cpp
        # parent_dir:  base-dir/user_codes/lang/uuid
        parent_dir = os.path.dirname(code_filepath)

        # create the container
        container_error_message, data = code_container.run_container(
            user_file_parent_dir=parent_dir
        )

        # no error in docker. now data dict contains data, else data is an empty dict.
        if container_error_message is None:
            status_code = data.get("status_code")
            status = data.get("status")
            error_message = data.get("error_message")
            success_message = data.get("success_message")

            # output is written in output.txt. check output.txt to compare with testcase.txt
            if status_code == 0:
                result = compare_test_cases(output_filepath, testcases_flepath)
                print("Code Run Successful.")
                print("status_code: ", status_code)
                print("status: ", status)
                print("error message: ", error_message)
                print("success message: ", success_message)
            else:  #  compilation error or other error. output.txt is empty. 
                formatted_error_message = format_error_message(error_message=error_message)
                print("Code Run Unsuccessful.")
                print("status_code: ", status_code)
                print("status: ", status)
                print("formatted error message: ", formatted_error_message)
                print("success message: ", success_message)
        else:  # some system and docker related error
            print("\n\n: Some Error Occurred: ")
            print(container_error_message)
    else:  # data write in file system is unsuccessfu.
        error_message = result[1]
        print("\nFile Write Error: ", error_message)


test_code_exec()
