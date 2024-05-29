"""
Django settings for rcee project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import environ

env = environ.Env()

# TODO CHANGE {ENVIRONMENT_TYPE} to PROD Environment
ENVIRONMENT_TYPE = ".dev"

# this effectively pointing to the SRC dir where the manage.py file is located.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# read all dependable .envs
env.read_env(Path(str(BASE_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.django")
env.read_env(Path(str(BASE_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.postgres")

# core_apps entrypont
APP_DIR = BASE_DIR / "core_apps"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG")
if DEBUG == "True":
    DEBUG = True
else:
    DEBUG = False

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


THIRD_PARTH_APPS = [
    "rest_framework",
    "corsheaders",
]

LOCAL_APPS = ["core_apps.common", "core_apps.mq_manager", "core_apps.rce_engine"]


# installed apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTH_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "rcee.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "rcee.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# TODO set prod Database
# DATABASES = {"default": env.db("DATABASE_URL")}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

# admin url
ADMIN_URL = env("ADMIN_URL")
# CORS_URLS_REGEX = r"^api/.*$"

# JWT Signing Key
JWT_SIGNING_KEY = env("JWT_SIGNING_KEY")

# static and media urls
STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "mediafiles")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


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
    "loggers": {
        "django.db": {
            "level": "DEBUG",
            "handlers": ["console"],
        }
    },
}
