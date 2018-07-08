#!/usr/bin/env python3
"""
Hardcoded script for connecting the rotator to hamlib

Run stitcher.sh before this and unstitcher.sh after

author: Marion Anderson
date:   2018-06-12
file:   interface.py
"""
from __future__ import absolute_import, print_function

import os

import serial

from rotator import Rotator

# Rotator setup
rot = Rotator()
rot.attach(23, 24, 27)  # from my soldershield design
homedir = os.environ['HOME']
ser = serial.Serial(port=homedir + '/.satcomm/ttySatR',
                    baudrate=38400, timeout=0.5)

# Reading input and Commanding servos
while True:
    try:
        serdata = ser.readlines()
        if len(serdata) < 1:  # don't try to parse a lack of commands
            continue

        # parse input
        cmdstr = serdata[-1].decode('utf-8')[0:-2]  # get last instruction
        az_str, el_str = cmdstr.split(' ')[0:2]
        az_angle = int(float(az_str[2:]))  # fmt: AZxxx.x
        el_angle = int(float(el_str[2:]))  # fmt: ELxxx.x

        # execute
        # TODO: Conver az-el coordinates to servo angles
        print('Az', az_angle, 'El', el_angle)
        rot.write(az_angle, el_angle)

    # if something goes wrong with the serial port, just exit
    # user likely closed the port and
    # there's probably no need for a long stack trace
    except serial.SerialException:
        print('Serial port closed unexpectedly!')
        break

    # There is no need for a delay or sleep command at loop end because
    # Serial.readline causes a delay on its own.
    # From the PySerial documentation, readline waits for the timeout to expire
    # before returning read data from the serial port.
