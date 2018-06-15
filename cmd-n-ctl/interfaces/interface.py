#! /home/pi/mySatComm/satcomm/bin/python3.5
"""
Experimental interface script for hamlib.

Run stitcher.sh before this and unstitcher.sh after

author: Marion Anderson
date:   2018-06-12
file:   interface.py
"""
from __future__ import print_function, absolute_import
import serial
from sainsmart import SainSmart

# servos
azServo = SainSmart()
azServo.attach(18)
elServo = SainSmart()
elServo.attach(20)

# serial port initialization
ser = serial.Serial(port='/dev/ttyS11', baudrate=38400, timeout=0.5)

while True:
    try:
        serdata = ser.readlines()
        if len(serdata) < 1:
            continue

        # parse
        cmdstr = serdata[-1].decode('utf-8')[0:-2]  # get last instruction
        az, el = cmdstr.split(' ')[0:2]
        az = az[2:]  # fmt: AZxxx.x
        el = el[2:]  # fmt: EXxxx.x

        # execute
        # TODO: Conver az-el coordinates to servo angles
        print('cmdstr =', cmdstr)
        print('serdata =', serdata)
        print('az =', az, 'el =', el)
        print()
        # no need for time.sleep() because readlines uses ser.timeout for delay
    except serial.SerialException:
        print('Serial port closed')
        break
