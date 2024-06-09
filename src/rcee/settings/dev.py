from .base import *  # noqa
from .base import env  # noqa: E501

# warnigns for linters code - E501 for unused variables

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

ALLOWED_HOSTS = ["127.0.0.1"]

# Config for MQ: Code Submission Consume
CLOUD_AMQP_URL = env("CLOUD_AMQP_URL")
CPP_CODE_SUBMISSION_EXCHANGE_NAME = env("CPP_CODE_SUBMISSION_EXCHANGE_NAME")
CPP_CODE_SUBMISSION_EXCHANGE_TYPE = env("CPP_CODE_SUBMISSION_EXCHANGE_TYPE")
CPP_CODE_SUBMISSION_QUEUE_NAME = env("CPP_CODE_SUBMISSION_QUEUE_NAME")
CPP_CODE_SUBMISSION_BINDING_KEY = env("CPP_CODE_SUBMISSION_BINDING_KEY")
CPP_CODE_SUBMISSION_ROUTING_KEY = env("CPP_CODE_SUBMISSION_ROUTING_KEY")

# Config for MQ: Result Publish Produce
RESULT_PUBLISH_EXCHANGE_NAME = env("RESULT_PUBLISH_EXCHANGE_NAME")
RESULT_PUBLISH_EXCHANGE_TYPE = env("RESULT_PUBLISH_EXCHANGE_TYPE")
RESULT_PUBLISH_QUEUE_NAME = env("RESULT_PUBLISH_QUEUE_NAME")
RESULT_PUBLISH_BINDING_KEY = env("RESULT_PUBLISH_BINDING_KEY")
RESULT_PUBLISH_ROUTING_KEY = env("RESULT_PUBLISH_ROUTING_KEY")


# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s  %(process)d %(thread)d %(message)s "
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    # uncomment for django database query logs
    # "loggers": {
    #     "django.db": {
    #         "level": "DEBUG",
    #         "handlers": ["console"],
    #     }
    # },
}
