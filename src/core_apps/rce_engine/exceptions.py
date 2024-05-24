from docker.errors import DockerException


class TimeLimitExceedException(DockerException):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        base_message = super().__str__()
        if self.status_code is not None:
            return f"{base_message} (status_code: {self.status_code})"
        return base_message
