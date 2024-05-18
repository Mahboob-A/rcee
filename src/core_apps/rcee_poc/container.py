import os, json, logging

import docker
from docker.errors import (
    ContainerError,
    ContextNotFound,
    APIError,
    ImageNotFound,
    ImageLoadError,
)

logger = logging.getLogger(__name__)

client = docker.from_env()


class CodeContainer:
    """Container class to spawn docker container to execute user code."""

    def run_container(self, user_file_parent_dir: str):  # base-dir/user_codes/lang/uuid
        """Run a container to compile and run user code in secure docker environment.

        Args:
          The host directory where the user codes files are created.

        Return:
          container_error_message:
            if try block is true, container_error_message is None
            if except block is true, contains the respective contianer error message.

          data {status, status_code, error_message, success_message}:
              if try block is true, contains the user code run result, including any g++ errors.
              if no compilation error, the output is saved in the output.txt file.

        """

        # if the try block is true, then irrespective of status_code of the program
        # the message will indicate a successful code run.
        # but message does not dictate if any compilation error happened.
        # the data dict will have the detailes of the resullt of the program.
        container_error_message = None 
        data = {}
        try:
            cont = client.containers.run(
                image="algocode/cpp-image",
                volumes={
                    f"{user_file_parent_dir}/": {
                        "bind": "/user-codes/cpp/result",
                        "mode": "rw",
                    }
                },
                detach=True,
            )
            # result of the run.
            result = cont.wait()
            logs = cont.logs().decode("utf-8")
            status_code = result.get("StatusCode")

            # Compilation Error
            if status_code != 0:
                data = {
                    "status": "compilation error",
                    "status_code": status_code,
                    "error_message": logs,
                    "success_message": None,
                }
            else:
                data = {
                    "status": "successful",
                    "status_code": status_code,
                    "error_message": None,
                    "success_message": "code compiled and run successfully.",
                }
        except ContainerError as e:
            container_error_message = f"\nContainerError: \n{str(e)}"
        except ContextNotFound as e:
            container_error_message = f"\nContextNotFound: \n{str(e)}"
        except APIError as e:
            container_error_message = f"\nAPIError: \n{str(e)}"
        except ImageNotFound as e:
            container_error_message = f"\nImageNotFound: \n{str(e)}"
        except ImageLoadError as e:
            container_error_message = f"\nImageLoadError: \n{str(e)}"
        except Exception as e:
            container_error_message = f"\nUnexpected Error Occurred: \n{str(e)}"
        finally:
            cont.remove()

        # return result to caller.
        return container_error_message, data


code_container = CodeContainer()
