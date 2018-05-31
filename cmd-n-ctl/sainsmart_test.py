#! /usr/bin/env python
"""
Script for testing SainSmart class servo interface and timing

author: Marion Anderson
date:   2018-05-30
file:   sainsmart_test.py
"""
from future import print_function, absolute_import
from sainsmart import SainSmart

from sys import argv, exit
from time import sleep

from random import uniform


myServo = SainSmart()

if __name__ == '__main__':
    myServo.attach(23)

    # Move to neutral position (test)
    myServo.write(1500)
    print('myServo moved to 1500us! Wait 5s...')
    sleep(5)

    # Resetting pulsewidth to 0
    myServo.write(0)
    print('myServo set to 0us! Wait 5s...')
    sleep(5)

    # Setting servo to random position
    pos = uniform(500, 2500)
    myServo.write(pos)
    print('myServo written to {0:}us! Wait 0.1s...'.format(pos))
    sleep(0.1)

    # Resetting pulsewidth to 0
    myServo.write(0)
    print('myServo written to 0us! wait 3s...')
    sleep(3)

    # Releasing resources and exiting
    myServo.detach()
    exit(0)
