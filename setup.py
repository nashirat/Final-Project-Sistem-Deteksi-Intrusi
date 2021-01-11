#!/usr/bin/env python

import re
import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = 'sul.remote-integrity'
SLUG = NAME.replace('-', '_')
PATH = SLUG.replace('.', os.path.sep)
NAMESPACE = 'sul'

DESCRIPTION = (
    'IDS yang berfungsi untuk membaca file yang ditambah, diubah, atau dihapus pada server.'
    )

URL = ''
EMAIL = 'nashir1187@gmail.com'
AUTHOR = 'Sulthon Nashir'
REQUIRES_PYTHON = '>=3.5.0'

REQUIRED = [
    'appdirs==1.4.0',
    'axel==0.0.7',
    'certifi==2017.1.23',
    'cffi==1.9.1',
    'colorama==0.3.7',
    'colorlog==2.10.0',
    'cryptography==1.7.2',
    'future==0.16.0',
    'idna==2.2',
    'packaging==16.8',
    'paramiko==2.1.6',
    'pyasn1==0.2.1',
    'pycparser==2.17',
    'pyparsing==2.1.10',
    'python-telegram-bot==5.3.0',
    'six==1.10.0',
    'SQLAlchemy==1.3.0',
    'tabulate==0.7.7',
    'urllib3>=1.23',
    'virtualenv==15.1.0',
]

EXTRAS_REQUIRE = {
    'dev': [
        'twine',
        'wheel',
        'setuptools>=40.6.3'
    ]
}

ENTRY_POINTS = {
    'console_scripts': [
        'remote-integrity=sul.remote_integrity.__main__:main',
    ]
}
here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, PATH, '__init__.py'), encoding='utf-8') as init:
    VERSION = re.search(r'__version__ = [\'"]([\d.]+)[\'"]', init.read()).group(1)
    
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


setup(
    name=NAME,
    namespace_packages=[NAMESPACE],
    packages=[SLUG],
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    install_requires=REQUIRED,
    include_package_data=True,
    version=about['__version__'],
)
