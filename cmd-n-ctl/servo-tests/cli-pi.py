#! /usr/bin/env python3
"""
CLI for testing

author: Marion Anderson
date:   2018-06-16
file:   cli-pi
"""
from __future__ import absolute_import, print_function

import pigpio

pi = pigpio.pi()
pi.set_mode(18, pigpio.OUTPUT)
while True:
    val = float(input('Enter us value: '))
    pi.set_servo_pulsewidth(18, val)
