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


# Config for CloudAMQP
CLOUD_AMQP_URL = env("CLOUD_AMQP_URL")
EXCHANGE_NAME = env("EXCHANGE_NAME")
EXCHANGE_TYPE = env("EXCHANGE_TYPE")
QUEUE_NAME = env("QUEUE_NAME")
BINDING_KEY = env("BINDING_KEY")
ROUTING_KEY = env("ROUTING_KEY")
