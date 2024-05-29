# exec_engine.py

import logging
import os

from core_apps.rce_engine.compare_testcases import TestcaseCompare
from core_apps.rce_engine.containers import CodeContainer
from core_apps.rce_engine.file_data_processor import FileDataProcessor
from core_apps.rce_engine.singleton import SingletonMeta

logger = logging.getLogger(__name__)


class CodeExecutionEngineHandler:
    """Handler class that acts as manager between File Write and Container Execution."""

    def __init__(self) -> None:
        self.__file_processor = FileDataProcessor()
        self.__code_container = CodeContainer()

    def __get_formatted_messages(
        self,
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

    def _exec_code(self, user_codes: dict, submission_id: str):
        """Handler method for core execution engine"""
        # write the user codes in file system
        result = self.__file_processor.write_data(
            data=user_codes, submission_id=submission_id
        )

        write_success = result[0]

        # if not None: data write in filesystem is successful.
        if write_success is not None:
            (
                code_filepath,
                input_filepath,
                output_filepath,
                testcases_filepath,
                file_write_message,
            ) = result[1:]

            # code_filepath:  base-dir/user_codes/lang/uuid/main.cpp
            # parent_dir:  base-dir/user_codes/lang/uuid
            # /app/user-files/user_codes/cpp/uuid
            parent_dir = os.path.dirname(code_filepath)

            # create the container, run the user code, and get the result dict.
            container_error_message, data = self.__code_container.run_container(
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
                    verdict = TestcaseCompare.compare_output_and_testcases(
                        output_filepath=output_filepath,
                        testcases_filepath=testcases_filepath,
                    )
                    return_data = self.__get_formatted_messages(
                        status_code=status_code,
                        status=status,
                        success_message=success_message,
                        error_message=error_message,
                        verdict=verdict,
                    )
                else:  #  compilation error or other error. output.txt is empty.
                    return_data = self.__get_formatted_messages(
                        status_code=status_code,
                        status=status,
                        success_message=success_message,
                        error_message=error_message,
                    )

            # some system and docker related error, TLE, Memory LImit etc.
            else:
                if data.get("status_code") == 124:
                    return_data = self.__get_formatted_messages(
                        status_code=status_code,
                        status=status,
                        success_message=success_message,
                        error_message=error_message,
                    )
                else:
                    #  Delete the created files.
                    self.__file_processor.del_user_dirs_files(
                        filepath=parent_dir, submission_id=submission_id
                    )
                    return container_error_message

            #  Delete the created files before returning the result. pass any filepath to delete all the files along with the unique uuid user dir.
            self.__file_processor.del_user_dirs_files(
                filepath=code_filepath, submission_id=submission_id
            )
            return return_data

        else:  # data write in file system is unsuccessfu.
            error_message = result[1]
            logger.exception(f"\n\nFile Write Error: {error_message}")
            return f"File Write Error: {error_message}"


class CodeExecutionEngine(CodeExecutionEngineHandler, metaclass=SingletonMeta):
    """Main Entrypoint for the Code Execution Engine
    CodeExecutionEngine is a Singleton class.
    """

    def exec_code(self, user_codes: dict, submission_id: str):
        """Main entrypont method to run code execution.

        Args:
            Dict: user codes, input.txt, testcases.txt
            Str: submission_id for the user code submission

        Return:
            Dict:
                Execution Result:
                    data:{status_code, status, success_message, error_message, {data:None{result: result, verdict}}
        """
        return self._exec_code(user_codes=user_codes, submission_id=submission_id)


# Object to import
code_execution_engine = CodeExecutionEngine()

if __name__ == "__main__":
    pass
