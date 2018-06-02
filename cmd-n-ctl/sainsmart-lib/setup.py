#! /usr/bin/env python3
"""
Package install script for SainSmart servo class on Raspberry Pi

Author: Marion Anderson
Date:  2018-06-01
"""

from setuptools import setup

setup(
    name='sainsmart',
    version='0.1.0',
    description='Python interface to SainSmart servos via Raspberry Pi',
    url='http://github.com/lmander42/mySatComm/',
    author='lmander42',
    license='MIT',
    py_modules=['sainsmart'],
    install_requires=['pigpio'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Raspian"
    ),
)
