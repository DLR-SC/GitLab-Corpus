# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

from setuptools import setup

setup(
    entry_points='''
        [console_scripts]
        corpus=corpus:cli
    '''
)
