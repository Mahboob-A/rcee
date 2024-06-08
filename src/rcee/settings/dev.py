from .base import *  # noqa
from .base import env  # noqa: E501

# warnigns for linters code - E501 for unused variables

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-7s1m)m)#ogw5qcv3yq=wl9-k%#ggd@-470b!=^$h-e-62ul3)k",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

ALLOWED_HOSTS = ["127.0.0.1"]


# Config for S3 to upload User Code Data to S3 Bucket from code-submit app.
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = env("AWS_LOCATION")


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
