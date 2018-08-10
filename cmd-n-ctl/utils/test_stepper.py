#!/usr/bin/env python3
"""Simple CLI for stepping a stepper motor

STEP PIN: 17
DIR PIN:  18

author: Marion Anderson
date:   2018-08-09
file:   test_stepper.py
"""
from __future__ import absolute_import

import time

import click
import pigpio


@click.command()
def main():
    """Steps a stepper motor and can change the direction."""
    print('Starting steppertest!')

    pi = pigpio.pi()
    pi.set_mode(18, pigpio.OUTPUT)
    pi.set_mode(17, pigpio.OUTPUT)
    pi.write(17, 1)

    # control
    state = 1
    go = True
    while go:
        cmd = input('Press enter to step or \'-\' to switch direction: ')
        # Direction
        if cmd == '-':
            if state == 1:
                pi.write(17, 0)
                state = 0
            else:
                pi.write(17, 1)
                state = 1
        # Exiting
        elif cmd == 'q' or cmd == 'quit' or cmd == 'exit':
            go = False
        # Stepping
        pi.write(18, 1)
        time.sleep(0.005)
        pi.write(18, 0)
        time.sleep(0.005)

    # Shutdown
    pi.stop()

if __name__ == '__main__':
    main()
