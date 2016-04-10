#!python
# coding=utf-8
from setuptools import setup, find_packages

setup(
    name = 'qqlib',
    version = '1.0',
    packages = find_packages(exclude=['test']),
    install_requires = [
        'rsa',
        'requests',
    ],
    author = 'Gerald',
    author_email = 'i@gerald.top',
    description = 'QQ lib for Python.',
    url = 'https://github.com/gera2ld/qqlib',
)
