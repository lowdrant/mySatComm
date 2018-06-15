#! /usr/bin/env python3
"""
A script for testing the SainSmart class servo interface and timing.

The servo should be connected to pin 18. Otherwise change line 22 of this file.

author: Marion Anderson
date:   2018-05-30
file:   sainsmart_test.py
"""
from __future__ import print_function, absolute_import
from time import sleep
from random import uniform

from sainsmart import SainSmart

myServo = SainSmart()

if __name__ == '__main__':
    myServo.attach(18)

    # Move to extrema and neutral positions
    for pos in (500, 1500, 2500):
        myServo.write(pos)
        print('myServo moved to {}us! Wait 2s...'.format(pos))
        sleep(2)

    # Setting servo to random position
    pos = uniform(500, 2500)
    myServo.write(pos)
    print('myServo written to {0:}us! Wait 0.1s...'.format(pos))
    sleep(0.1)

    # Releasing resources and exiting
    myServo.detach()
    exit(0)
