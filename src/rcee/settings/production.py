from .base import *  # noqa
from .base import env  # noqa: E501

# warnigns for linters code - E501 for unused variables


# Django project general settings.
ADMINS = [("Mahboob Alam", "iammahboob.a@gmail.com")]
SECRET_KEY = env("DJANGO_SECRET_KEY")
ADMIN_URL = env("ADMIN_URL")
DATABASES = {"default": env.db("DATABASE_URL")}


# Django security settings.
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["rcee.algocode.site"])

CSRF_TRUSTED_ORIGINS = ["https://rcee.algocode.site", "https://algocode.site"]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = env("DJANGO_SECURE_SSL_REDIRECT", default=True)


# TODO caution. 518400 seconds as 6 days. use wisely.
SECURE_HSTS_SECONDS = 60

SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)

SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)

# Static file content host
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SITE_NAME = "Algocode - The Modern Leetcode!"


########################################################
# logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequieDebugFalse"}},
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
