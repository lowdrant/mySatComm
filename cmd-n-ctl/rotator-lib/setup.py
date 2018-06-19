#! /usr/bin/env python3
"""
Package install script for Rotator servo class on Raspberry Pi

Author: Marion Anderson
Date:  2018-06-17
"""
from __future__ import absolute_import

from setuptools import setup

setup(
    name='rotator',
    version='0.1.0',
    description='Python interface to SainSmart servos via Raspberry Pi',
    url='http://github.com/lmander42/mySatComm/cmd-n-ctl/rotator-lib',
    author='lmander42',
    license='MIT',
    py_modules=['rotator'],
    install_requires=['pigpio'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Raspian"
    ),
)
