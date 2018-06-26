#! /usr/bin/env python3
"""
Tests rotator - prompts user for interface

author: Marion Anderson
date:   2018-06-25
file:   rotator_prompt.py
"""
from __future__ import absolute_import, print_function

from rotator import Rotator

# Rotator setup
rot = Rotator()
rot.attach(23, 22, 24)

# Reading input and Commanding servos
while True:
    az_str = input('Enter an azimuth angle: ')
    el_str = input('Enter an elevation angle: ')

    # parse input
    az_angle = int(az_str)
    el_angle = int(el_str)

    # execute
    print('az =', az_angle, 'el =', el_angle)
    rot.write(az_angle, el_angle)
