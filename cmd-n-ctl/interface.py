#! /usr/bin/env python3
"""
Experimental interface script for hamlibself.

Run stitcher.sh before this and unstitcher.sh after

author: Marion Anderson
date:   2018-06-12
file:   interface.py
"""
from time import sleep
from sainsmart import SainSmart
import serial

# servo initialization
azServo = SainSmart()
azServo.attach(18)
elServo = SainSmart()
elServo.attach(20)

# serial port initialization
ser = serial.Serial('/dev/ttyS11', baudrate=38400, timeout=1)

while True:
    # get input
    input = ser.readlines()
    cmdstr = input[-1]  # get last instruction
    print(input, cmdstr)

    # parse
    az, el = cmdstr.split(' ')[0:1]
    az = az[2:]  # fmt: AZxxx.x
    el = el[2:]  # fmt: EXxxx.x

    # execute
    print('az =', az, 'el =', el)
    # azServo.write(az)
    # elServo.write(el)
    # TODO: Conver az-el coordinates to servo angles

    sleep(0.5)  # wait half a second between readings
