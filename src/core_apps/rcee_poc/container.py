import os, json, logging, time

import docker
from docker.errors import (
    ContainerError,
    ContextNotFound,
    APIError,
    ImageNotFound,
    ImageLoadError,
)

from exceptions import TimeLimitExceedException

logger = logging.getLogger(__name__)

client = docker.from_env()


class CodeContainerHandler:
    """Container Handler class to spawn docker container to execute user code."""

    def __get_current_time(self):
        """Return current time to measure container runtime"""
        return time.time()

    def __get_formated_data(self, status_code: int, logs: str):
        """Return formated docker stdout and stderr data"""

        data = {}
        # Container Exit Code
        if status_code == 0:
            data = {
                "status": "Successful",
                "status_code": status_code,
                "error_message": None,
                "success_message": "code compiled and run successfully.",
            }
        elif status_code == 124:
            data = {
                "status": "Time Limit Exceed",
                "status_code": status_code,
                "error_message": logs,
                "success_message": None,
            }
        elif status_code == 137:
            data = {
                "status": "Memory Limit Exceed",
                "status_code": status_code,
                "error_message": logs,
                "success_message": None,
            }
        elif status_code == 139:
            data = {
                "status": "Index Out Of Bound",
                "status_code": status_code,
                "error_message": logs,
                "success_message": None,
            }
        else:
            # Memory Limit Exceed
            if "g++: fatal error: Killed signal terminated program cc1plus" in logs:
                data = {
                    "status": "Runtime Error",
                    "status_code": 137,
                    "error_message": "Memory Limit Exceed",
                    "success_message": None,
                }
            else:  # other compilation error
                data = {
                    "status": "Compilation Error",
                    "status_code": status_code,
                    "error_message": logs,
                    "success_message": None,
                }
        return data

    def _run_container(
        self, user_file_parent_dir: str
    ):  # base-dir/user_codes/lang/uuid
        """Handler method to spawn container."""
        # if the try block is true, then irrespective of status_code of the program
        # the message will indicate a successful code run.
        # but message does not dictate if any g++ related compilation or other error happened.
        # the data dict will have the details of the resullt of the program.

        start_time = self.__get_current_time()
        container_error_message = None
        data = {}
        cont_ulimits = [
            {"Name": "nproc", "Soft": 25, "Hard": 50},  # no of process
            {
                "Name": "nofile",
                "Soft": 25,
                "Hard": 50,
            },  # no of open descriptors like file
        ]
        security_opt = ["seccomp=default"]
        try:
            cont = client.containers.run(
                image="algocode/cpp-image:latest",
                volumes={
                    f"{user_file_parent_dir}/": {
                        "bind": "/user-codes/cpp/result",
                        "mode": "rw",
                    }
                },
                detach=True,
                privileged=False,
                network_disabled=True,
                mem_limit="520m",
                mem_reservation="300m",
                memswap_limit="600m",
                mem_swappiness=0,
                # cpus="1.0",  # does not work.
                cpu_period=100000,  # total 1 cpu. 100 miliseconds
                cpu_quota=100000,
                pids_limit=500,
                ulimits=cont_ulimits,
                # security_opt=["seccomp", "default"],
            )

        # long polling 
        # short polling 
        # server sent event: sse 

            try:
                cont.reload()
                result = cont.wait(timeout=5)
            except Exception as e:
                # Normal program should complete before the timeout in .wait()
                # if the container exit after timeout, indicates TLE.
                cont.stop(timeout=0)
                raise TimeLimitExceedException("Time Limit Exceed", status_code=124)

            cont.reload()
            logs = cont.logs().decode("utf-8")
            status_code = result.get("StatusCode")
            # print(cont.attrs)

            # formatted data. as control here, the code compiled and run.
            data = self.__get_formated_data(status_code=status_code, logs=logs)

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
        except TimeLimitExceedException as e:
            container_error_message = f"\nTimeLimitExceedException: \n{str(e)}"
            data = {
                "status": "Runtime Error",
                "status_code": 124,
                "error_message": "Time Limit Exceed",
                "success_message": None,
            }
        except Exception as e:
            container_error_message = f"\nUnexpected Error Occurred: \n{str(e)}"
        finally:
            cont.stop(timeout=0)
            cont.remove()

        # FIXME Time DEBUG. Delete.
        end_time = self.__get_current_time()
        print("\n\nTime Taken Inside Container: ", end_time - start_time)

        return container_error_message, data


class CodeContainer(CodeContainerHandler):
    """Container class to spawn docker container to execute user code."""

    def run_container(self, user_file_parent_dir: str):
        """Entrypoint method - Run a container to compile and run user code in secure docker environment.

        Args:
          The host directory where the user codes files are created.

        Return:
          container_error_message:
            if try block is true, container_error_message is None. Code run successful.
            if except block is true, contains the respective contianer error message. TLE Exception caught in this case.

          data {status, status_code, error_message, success_message}:
              if try block is true, contains the user code run result, including any g++ errors.
              if no compilation error, the output is saved in the output.txt file.
        """
        container_error_message, data = self._run_container(
            user_file_parent_dir=user_file_parent_dir
        )
        return container_error_message, data


# object.
code_container = CodeContainer()
