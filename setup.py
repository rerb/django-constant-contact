#!/usr/bin/env python
from setuptools import setup
import os


# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-constant-contact',
    version='1.0',
    description=("Django package for creating email marketing "
                 "campaigns in Constant Contact"),
    author='Bob Erb',
    author_email='bob.erb@aashe.org',
    url='https://github.com/aashe/django-constant-contact',
    long_description=read("README.md"),
    packages=[
        'django_constant_contact',
        'django_constant_contact.migrations'
    ],
    install_requires=[
        "Django>=1.7,<1.9",
        'django-jsonfield==0.9.15',
        'nap==2.0.0',
        'premailer==2.10.1',
        'requests==2.9.1',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    test_suite='tests.main',
)
