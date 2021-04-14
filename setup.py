# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

from setuptools import setup

setup(
    name='corpus',
    version='0.1',
    py_modules=['corpus'],
    install_requires=[
        'Click',
        'python-gitlab',
        'sphinx',
        'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        corpus=corpus:cli
    ''',
)
