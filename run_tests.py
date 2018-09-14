#!/usr/bin/env python
import os
import sys

import django
import dj_database_url


BASE_PATH = os.path.dirname(__file__)


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation
    http://www.djangosnippets.org/snippets/1044/
    """
    sys.exc_clear()

    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.contenttypes',
        'django_constant_contact',
    )

    global_settings.DATABASES = {'default': dj_database_url.config()}

    global_settings.MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware'
    )

    # custom settings for tests
    global_settings.CONSTANT_CONTACT_API_KEY = os.environ.get(
        'CONSTANT_CONTACT_API_KEY', None)
    global_settings.CONSTANT_CONTACT_ACCESS_TOKEN = os.environ.get(
        'CONSTANT_CONTACT_ACCESS_TOKEN', None)
    global_settings.CONSTANT_CONTACT_FROM_EMAIL = os.environ.get(
        'CONSTANT_CONTACT_FROM_EMAIL', None)
    global_settings.CONSTANT_CONTACT_REPLY_TO_EMAIL = os.environ.get(
        'CONSTANT_CONTACT_REPLY_TO_EMAIL', None)
    global_settings.CONSTANT_CONTACT_USERNAME = os.environ.get(
        'CONSTANT_CONTACT_USERNAME', None)
    global_settings.CONSTANT_CONTACT_PASSWORD = os.environ.get(
        'CONSTANT_CONTACT_PASSWORD', None)

    global_settings.SECRET_KEY = "blahblah"

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    django.setup()

    if django.VERSION > (1, 2):
        test_runner = test_runner()
        failures = test_runner.run_tests(['django_constant_contact', ])
    else:
        failures = test_runner(['django_constant_contact', ], verbosity=1)
    sys.exit(failures)

if __name__ == '__main__':
    main()
