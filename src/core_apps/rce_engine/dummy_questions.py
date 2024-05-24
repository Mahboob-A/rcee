# few questions with input and testcases to test the engine

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

sum_of_a_b_problem = {
    "lang": "cpp",
    "code": "#include <bits/stdc++.h>\nusing namespace std; \n\nvoid sum_of_a(int a, int b)\n{\n    cout << a + b << endl; \n}\n\n\nint main()\n{\n    int t, a, b; \n    cin >> t; \n    \n    while(t--)\n    {\n        cin >> a >> b; \n        sum_of_a_b(a, b); \n    }\n\n    return 0;\n}",
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
        "1000 2000",
    ],
    "testcases": ["3", "12", "10", "15", "30", "55", "200", "300", "200", "300"],
}


hello_world_with_num_data_problem = {
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
        "Hello World: 10",
    ],
}

time_limit_exceed_problem = {
    "lang": "cpp",
    "code": "//just a value is incremented infinitely\n\n#include <iostream>\n\nint main() {\n int a = 0; \n while(1) {\n a++;  \n  }\n\n  return 0;\n}",
    "input": ["10", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    "testcases": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "11"],
}


memory_limit_exceed_problem = {
    "lang": "cpp",
    "code": "//creates many long long array of large size\n\n#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n  int t, n;\n\n long long m = 100000;\n\n    while (1) {\n        long long arr[m]; \nm = m*5;\n   }\n\n  return 0;\n}",
    "input": ["10", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    "testcases": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "11"],
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
