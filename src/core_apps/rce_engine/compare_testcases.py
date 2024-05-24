# util func to compare testcase


class TestcaseCompare:
    def compare_output_and_testcases(output_filepath: str, testcases_filepath: str):
        """A function to compare testcases.txt againt output.txt of user submitted code.

        Args:
            Str: File path of output.txt and testcases.txt

        Return:
            Dict: Result of the comparison of the output.txt and testcases.txt
        """

        data = {}

        with open(output_filepath, "r") as output_file:
            output_content = output_file.read().strip().split("\n")

        with open(testcases_filepath, "r") as testcases_file:
            testcases_content = testcases_file.read().strip().split("\n")

        zip_content = list(
            zip(output_content, testcases_content)
        )  # Ex:  [('1 2', '1 2 '), ('3 4', '3 4'), ('5 6', '5 6')]
        # print('zip content: ', zip_content)

        for i, (output_line, testcases_line) in enumerate(zip_content):
            if output_line.strip() != testcases_line.strip():
                data["result"] = f"Wrong Answer at test case {i+1}"
                data["Output"] = f"{output_line}"
                data["Expected"] = f"{testcases_line}"
                data["verdict"] = "Wrong Answer"
                return data

        # if output and input file has different number of lines. WA
        if len(output_content) != len(testcases_content):
            data["result"] = "Output and test cases has different number of lines"
            data["output_file_length"] = f"{len(output_content)}"
            data["testcases_file_length"] = f"{len(testcases_content)}"
            data["verdict"] = "Wrong Answer"
            return data

        # all testcases passed.
        data["result"] = "All testcases passed"
        data["verdict"] = "Accepted"
        return data


testcase_comparer = TestcaseCompare()
if __name__ == "__main__":
    pass
