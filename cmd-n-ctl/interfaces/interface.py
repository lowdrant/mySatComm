#! /usr/bin/env python3
"""
Experimental script for rotator control with hamlib.
Reads from rotator_config.json

Run stitcher.sh before this and unstitcher.sh after

author: Marion Anderson
date:   2018-06-12
file:   interface.py
"""
from __future__ import absolute_import, print_function

import json
import os
import time

import serial

import rotator


def main():

    # Parse config
    with open('~/.satcomm/include/rotator_config.json') as f:
        config = json.load(f)
    pin_az1 = int(config['pin_az1'])
    pin_az2 = int(config['pin_az2'])
    pin_el = int(config['pin_el'])
    baudrate = config['baudrate']
    port = config['port']

    # Startup
    rot = rotator.Rotator()
    rot.attach(pin_az1, pin_az2, pin_el)
    ser = serial.Serial(port=port, baudrate=baudrate, timeout=0.25)

    # Execution
    while os.path.exists('~/satcomm_runflag_delete2stop'):
        try:
            serdata = ser.readlines()
            if len(serdata) < 1:  # don't try to parse a lack of commands
                continue

            # parse input
            cmdstr = serdata[-1].decode('utf-8')[0:-2]  # get last instruction
            az_str, el_str = cmdstr.split(' ')[0:2]
            az_angle = float(az_str[2:])  # fmt: AZxxx.x
            el_angle = float(el_str[2:])  # fmt: ELxxx.x

            # execute
            # TODO: Conver az-el coordinates to servo angles
            print('cmdstr =', cmdstr)
            print('serdata =', serdata)
            print('az =', az_angle, 'el =', el_angle)
            print()

            for i in range(4):  # "smooth out" servo movement
                rot.writeRotator()
                time.sleep(0.01)

        # if something goes wrong with the serial port, just exit
        # user likely closed the port and
        # there's probably no need for a long stack trace
        except serial.SerialException:
            print('Serial port closed unexpectedly!')
            break

    ser.close()
    rot.detach()


if __name__ == '__main__':
    main()
