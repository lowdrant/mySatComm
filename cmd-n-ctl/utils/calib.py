#!/usr/bin/env python3
"""
Runs rotator calibration sequence

author: Marion Anderson
date:   2018-07-29
file:   calib.py
"""
from __future__ import absolute_import, print_function

import os

import serial

from rotator import Rotator

# Rotator setup
rot = Rotator()
rot.attach(27, 23, 24)  # from my soldershield design
rot.calibrate()  # zero before doing anything
