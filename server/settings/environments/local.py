"""
Django Project - Local Environment Settings.

This file contains the settings that are specific to the local environment.
"""

from server.settings.components import BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ybbn6#(d=yi2kl(5^c2ah*j0vs&m6uz+(5u^9c4h-s$@z"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Media files
# https://docs.djangoproject.com/en/4.2/topics/files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
