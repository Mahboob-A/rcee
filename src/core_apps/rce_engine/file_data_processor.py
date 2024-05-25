import os
import logging

from core_apps.rce_engine.singleton import SingletonMeta

logger = logging.getLogger(__name__)


class FileDataProcessorHandler:
    """Handler class for FileDataProcessor class."""

    def __get_user_code_base_dir(self):
        """Return the base-dir/user_codes directory

        Storage:
            volume:
                name: user_code_files

        The below '$base_dir' is the volume mount for the Judge Container.
        The volume mount of sibling container is also same as the Main Judge Container.

        Hence, everything is saved under 'base_dir' in the Judge Container, will be available at
        the volume mount of sibling contianer.

        Ex: Judge Container file path: /app/user-files/user_codes/lang/uuid/
            Sibling Container file path for the same data: /app/user-files/user_codes/lang/uuid/
            As both has the mount point name same.
        """

        # this is the volume mount for the main Judge Container as well as sibling contianer.
        # see the docker compose file for main judge container, and "containers" module for sibling container.
        base_dir = "/app/user-files"

        user_code_dir = "user_files"
        user_code_base_dir = os.path.join(base_dir, user_code_dir)
        return user_code_base_dir

    def __get_user_code_base_dir_with_lang(self, lang: str):
        """return the base-dir/user_codes/{lang} directory"""

        user_code_base_dir = self.__get_user_code_base_dir()
        base_dir_with_lang = os.path.join(user_code_base_dir, lang)

        return base_dir_with_lang

    def _process_write_data(
        self,
        submission_id: str,
        lang: str,
        cpp_code: str,
        input_data: str,
        testcases_data: str,
    ):
        """write the user codes and testcases in the filesyste."""

        code_file_name = "main.cpp"
        input_file_name = "input.txt"
        output_file_name = "output.txt"
        testcases_file_name = "testcases.txt"
        error_message = ""
        success_message = "file-created"

        # lang path: base-dir/user_codes/lang/
        main_lang_dir = self.__get_user_code_base_dir_with_lang(lang=lang)

        # unique user main dir path: base-dir/user_codes/lang/uuid4
        main_user_file_dir = os.path.join(main_lang_dir, f"{submission_id}")

        try:
            # create the directories: base-dir/user_codes/lang/uuid4
            os.makedirs(main_user_file_dir)
            logger.info(f"Entrypoint of User's Unique Data Dir Judge Container Mount Point:  {main_user_file_dir}")
        except (FileExistsError, PermissionError, OSError, Exception) as e:
            logger.error(
                f"\n[ERROR: DIR CREATE FAILED]: Main User File Dir: {main_user_file_dir} Could Not Be Created To FIle System"
            )
            logger.exception(f"\n[EXCEPTION: {str(e)}]")
            error_message = "user-dir-create-error"
            return None, error_message
        


        # create files under main_user_file_dir: base-dir/user_codes/lang/uuid4
        try:
            # create the code file: base-dir/user_codes/lang/uuid4/main.cpp
            os.mknod(f"{main_user_file_dir}/{code_file_name}")

            # create input file: base-dir/user_codes/lang/uuid4/input.txt
            os.mknod(f"{main_user_file_dir}/{input_file_name}")

            # create the output file: base-dir/user_codes/lang/uuid4/output.txt
            os.mknod(f"{main_user_file_dir}/{output_file_name}")

            # create the testcases file: base-dir/user_codes/lang/uuid4/testcases.txt
            os.mknod(f"{main_user_file_dir}/{testcases_file_name}")
        except (PermissionError, OSError, Exception) as e:
            logger.error(
                f"\n[ERROR: FILE CREATE FAILED]: Something went wrong while creating user files in filesystem."
            )
            logger.exception(f"\n[EXCEPTION: {str(e)}]")
            error_message = "user-file-create-error"

            # delete the created dirs
            self._process_del_user_dirs_files(
                filepath=main_user_file_dir, submission_id=submission_id
            )
            return None, error_message

        # created paths of the files
        # the concatinated code filepath: base-dir/user_codes/lang/uuid4/main.cpp
        code_filepath = os.path.join(main_user_file_dir, code_file_name)

        # the concatinated input filepath: base-dir/user_codes/lang/uuid4/input.txt
        input_filepath = os.path.join(main_user_file_dir, input_file_name)

        # the concatinated output filepath: base-dir/user_codes/lang/uuid4/output.txt
        output_filepath = os.path.join(main_user_file_dir, output_file_name)

        # the concatinated testcases filepath: base-dir/user_codes/lang/uuid4/testcases.txt
        testcases_filepath = os.path.join(main_user_file_dir, testcases_file_name)

        # write the code data in the file: base-dir/user_codes/cpp/uuid/main.cpp
        try:
            # write the user code in the code_file_name.extention file
            with open(code_filepath, "w") as f:
                f.write(cpp_code)
        except Exception as e:
            logger.error(
                f"\n[ERROR: CODE WRITE IN FILE FAILED]: User Code File (main.cpp) Could Not Be Written To FIle System"
            )
            logger.exception(f"\n[EXCEPTION: {str(e)}]")
            error_message = "code-file-write-error"

            # delete all the created dirs
            self._process_del_user_dirs_files(
                filepath=code_filepath, submission_id=submission_id
            )
            return None, error_message

        # write the input data in the file: base-dir/user_codes/cpp/uuid/input.txt
        try:
            with open(input_filepath, "w") as f:
                f.write(input_data)
        except Exception as e:
            logger.error(
                f"\n[ERROR: INPUT WRITE IN FILE FAILED]: input.txt File Could Not Be Written To FIle System"
            )
            logger.exception(f"\n[EXCEPTION: {str(e)}]")
            error_message = "input-file-write-error"

            # delete all the created dirs
            self._process_del_user_dirs_files(
                filepath=input_filepath, submission_id=submission_id
            )
            return None, error_message

        # write the tesecases data in the file: base-dir/user_codes/cpp/uuid/testcases.txt
        try:
            with open(testcases_filepath, "w") as f:
                f.write(testcases_data)
        except Exception as e:
            logger.error(
                f"\n[ERROR: TESTCASES WRITE IN FILE FAILED]: testcases.txt File Could Not Be Written To FIle System"
            )
            logger.exception(f"\n[EXCEPTION: {str(e)}]")
            error_message = "testcases-file-write-error"

            # delete all the created dirs
            self._process_del_user_dirs_files(
                filepath=testcases_filepath, submission_id=submission_id
            )
            return None, error_message

        # return the file paths
        logger.info(
            f"\n\n\n\n[SUCCESS: ALL FILE CREATE]: All related files for submission ID {submission_id} CREATED Successfully."
        )
        return (
            True,
            code_filepath,
            input_filepath,
            output_filepath,
            testcases_filepath,
            success_message,
        )

    def _process_del_user_dirs_files(self, filepath: str, submission_id: str):
        """Delete the files in unique user dir and then the unique user dir."""
        try:

            # check if the filepath is an absolute file path like: base-dir/user-codes/cpp/uuid/main.cpp
            if os.path.isfile(filepath):
                # get the parent dir of the current file: base-dir/user-codes/lang/uuid <-
                parent_dir = os.path.dirname(filepath)
            else:  # the filepath is a parent directory like: base-dir/user-codes/lang/uuid
                # to get the absolute dir so that dirname always returns the base-dir/user-codes/lang/uuid directory
                # adding "/" otherwise, the parent dir might be: base-dir/user-codes/lang <-
                # hence, whether the filepath is a absolute filepath, or a parent dir, it gets the parent dir of: base-dir/user-codes/lang/uuid <-
                filepath = f"{filepath}/"
                parent_dir = os.path.dirname(filepath)

            # delete all the files in the parent dir.
            for filename in os.listdir(parent_dir):
                os.remove(os.path.join(parent_dir, filename))

            # delete the empty user directory: base-dir/user-codes/cpp/uuid
            os.rmdir(parent_dir)

            logger.info(
                f"\n\n[SUCCESS: DIR DELETE]: User Dir and all files of submission ID: {submission_id} DELETED Successfully!"
            )
            return True
        except Exception as e:
            logger.error(
                f"\n\b[ERROR: DIR DELETE]: User Dir and all files submission ID: {submission_id} DELETION Unsuccessful"
            )
            logger.exception(f"\n[EXCEPTION]: {str(e)}")
            return False


class FileDataProcessor(FileDataProcessorHandler, metaclass=SingletonMeta):
    """Write user code in service container file system.
    The image takes the files from service container to compile the code
    """

    def del_user_dirs_files(self, filepath: str, submission_id: str = None):
        """DELETE User Dirs and Files

        Args:
            Str:
                filepath: either the absolute filepath or the parent directory of the filepaht.
            Str:
                submission_id: the submission id of the user code submission.

        Return:
            Bool:
                True:
                    Unique user directory along with files are deleted.
                False:
                    Unique user directory along with files could not be deleted.
        """

        # submission id only for logging.
        if submission_id is None:
            submission_id = "SUBMISSION ID NOT PROVIDED"

        return self._process_del_user_dirs_files(
            filepath=filepath, submission_id=submission_id
        )

    def write_data(self, data: dict, submission_id: str):
        """Main entrypoint of class to write data in filesystem

        Args:
            Dict:
                data: payload from client as dict.
            Str:
                submission_id: Unique submission id for the code submission.

        Return:
            Bool:
                True:
                    True, Code File Path, Input File Path, Output File Path, Success Message
                False:
                    None, Error Message for Failure
        """
        if "lang" in data and "code" in data and data["lang"] == "cpp":
            cpp_code = data.get("code")

            lang = data.get("lang")
            input_data = data.get("inputs")
            test_cases_data = data.get("testcases")
            
            result = self._process_write_data(
                submission_id=str(submission_id),
                lang=lang,
                cpp_code=cpp_code,
                input_data=input_data,
                testcases_data=test_cases_data,
            )
            # a tuple of data.
            return result


# Object to process data
file_processor = FileDataProcessor()

if __name__ == "__main__":
    json_data = {
        "lang": "cpp",
        "code": '#include <iostream>\nusing namespace std;\n\nint main()\n{\n    cout << "Hello World" << endl;\n    return 0;\n}',
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
    }

    result = file_processor.write_data(json_data)

    if result[0] is not None:
        print("file created successfully!")
        code_filepath, input_filepath, output_filepath, message = (
            result[1],
            result[2],
            result[3],
            result[4],
        )
        print("code file path: ", code_filepath)
        print("\ninput file path: ", input_filepath)
        print("\noutput file path: ", output_filepath)
        print("\nmessage: ", message)

    else:
        print("file could not be created")
        error_msg = result[1]
        print("error messge is: ", error_msg)
