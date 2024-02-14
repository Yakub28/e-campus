"""
Django Project - Settings Module.

This module is responsible for loading the correct settings file based on the
environment variable DJANGO_ENV. The default value is 'local', so if you don't
specify the environment variable, the local settings will be loaded.

For more information, see the documentation:
https://django-split-settings.readthedocs.io/en/latest/
"""

from split_settings.tools import include

from server.settings.components import config

ENV = config("DJANGO_ENV", default="local") or "local"

base_settings = (
    "components/common.py",  # Common settings
    "components/restframework.py",  # Django REST framework
    # Select the right env:
    f"environments/{ENV}.py",
)

# Include settings:
include(*base_settings)
