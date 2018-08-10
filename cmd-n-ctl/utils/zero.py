#!/usr/bin/env python3
"""
CLI for zeroing the rotator.
Intended for testing and setup uses.

author: Marion Anderson
date:   2018-07-28
file:   zero.py
"""
from __future__ import absolute_import, print_function

import os

import serial

from rotator import Rotator

# Rotator setup
rot = Rotator()
rot.attach(17, 4, 18)  # from my soldershield design
rot.zero()  # zero before doing anything
