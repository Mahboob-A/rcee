from .base import *  # noqa
from .base import env  # noqa: E501

# warnigns for linters code - E501 for unused variables


# Django project general settings.
ADMINS = [("Mahboob Alam", "iammahboob.a@gmail.com")]
SECRET_KEY = env("DJANGO_SECRET_KEY")


# No need, as no direct connection with RCE Engine available.
# CSRF_TRUSTED_ORIGINS = ["https://rcee.algocode.site", "https://algocode.site"]
# ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["rcee.algocode.site"])


SITE_NAME = "Algocode - The Modern Leetcode!"

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


########################################################
# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s  %(asctime)s %(module)s  %(process)d %(thread)d %(message)s "
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "django.request": {  # only used when debug=false
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {  # only used when debug=false
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
    # uncomment for django database query logs
    # 'loggers': {
    #     'django.db': {
    #         'level': 'DEBUG',
    #         'handlers': ['console'],
    #     }
    # }
}
