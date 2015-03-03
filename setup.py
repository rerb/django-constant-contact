#!/usr/bin/env python
from setuptools import setup, find_packages
import os

# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-constant-contact',
    version='0.1',
    description="Django package for creating email marketing campaigns in Constant Contact",
    author='Bob Erb',
    author_email='bob.erb@aashe.org',
    url='https://github.com/aashe/django-constant-contact',
    long_description=read("README.md"),
    packages=[
        'django-constant-contact',
        'django-constant-contact.migrations'
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
    install_requires=['mailchimp', 'nap'],
)
