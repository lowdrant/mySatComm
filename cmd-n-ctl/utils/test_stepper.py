#!/usr/bin/env python3
"""Simple CLI for testing a stepper motor

author: Marion Anderson
date:   2018-08-09
file:   test_stepper.py
"""
from __future__ import absolute_import

import time

import click
import pigpio


@click.command()
@click.option('--step-pin', default=17,
              help='GPIO pin number connected to STEP on the driver')
@click.option('--dir-pin', default=18,
              help='GPIO pin number connected to DIRECTION on the driver')
def main(step_pin, dir_pin):
    """Steps a stepper motor and can change the direction."""
    print('Starting steppertest!')

    pi = pigpio.pi()
    pi.set_mode(step_pin, pigpio.OUTPUT)
    pi.set_mode(dir_pin, pigpio.OUTPUT)
    pi.write(dir_pin, 1)

    # control
    state = 1
    go = True
    while go:
        cmd = input('Press enter to step or \'-\' to switch direction: ')
        # Direction
        if cmd == '-':
            if state == 1:
                pi.write(dir_pin, 0)
                state = 0
            else:
                pi.write(dir_pin, 1)
                state = 1
        # Exiting
        elif cmd == 'q' or cmd == 'quit' or cmd == 'exit':
            go = False
        # Stepping
        pi.write(step_pin, 1)
        time.sleep(0.005)
        pi.write(step_pin, 0)
        time.sleep(0.005)

    # Shutdown
    pi.stop()

if __name__ == '__main__':
    main()
