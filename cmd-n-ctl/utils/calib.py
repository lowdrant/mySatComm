#!/usr/bin/env python3
"""
Runs rotator calibration sequence

author: Marion Anderson
date:   2018-07-29
file:   calib.py
"""
from __future__ import absolute_import, print_function

from rotator import Rotator

# Rotator setup
rot = Rotator(23, 17, 22)
rot.attach()
rot.calibrate()  # zero before doing anything
