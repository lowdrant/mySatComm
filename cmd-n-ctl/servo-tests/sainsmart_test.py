<<<<<<< HEAD:cmd-n-ctl/sainsmart_test.py
=======
#! /usr/bin/env python3
>>>>>>> 2e69a758b8840ecd2e68871d49223b60e8eb61d8:cmd-n-ctl/servo-tests/sainsmart_test.py
"""
A script for testing the SainSmart class servo interface and timing.

author: Marion Anderson
date:   2018-05-30
file:   sainsmart_test.py
"""
<<<<<<< HEAD:cmd-n-ctl/sainsmart_test.py

=======
from __future__ import print_function, absolute_import
>>>>>>> 2e69a758b8840ecd2e68871d49223b60e8eb61d8:cmd-n-ctl/servo-tests/sainsmart_test.py
from sainsmart import SainSmart

from sys import exit
from time import sleep

from random import uniform

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
