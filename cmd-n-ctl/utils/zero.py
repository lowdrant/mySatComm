#!/usr/bin/env python3
"""
CLI for zeroing the rotator.
Intended for testing and setup uses.

author: Marion Anderson
date:   2018-07-28
file:   zero.py
"""
from __future__ import absolute_import, print_function

from rotator import Rotator

# Rotator setup
rot = Rotator()
rot.attach(23, 17, 22)  # from my soldershield design
rot.zero()  # zero before doing anything
