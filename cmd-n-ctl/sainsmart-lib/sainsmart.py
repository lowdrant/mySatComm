#! /usr/bin/env python3
"""
Object file for class interfacing with SainSmart319 servos

author: Marion Anderson
date:   2018-05-30
file:   sainsmart.py
"""
from __future__ import print_function, absolute_import
from time import sleep
import pigpio


# TODO: Allow attachment to pin at initialization
class SainSmartClassException(Exception):
    """Provide exceptions for SainSmart class"""
    pass


class SainSmart(object):
    """Interface to SainSmart 318 and 319 servomotors using PiGPIO.

    See this link for PiGPIO documentation:
    http://abyz.me.uk/rpi/pigpio/index.html

    See this link for SainSmart319 documentation:
    https://www.sainsmart.com/collections/robotics-cnc/products/copy-of-all-purpose-digital-servo-sr318
    """

    def __init__(self, freq=50, pin=None):
        """Creates basic instance of SainSmart object.

        :param freq: Frequency (Hz) of servo operation (Default 50)
        :param pin:  Broadcom pin number servo is attached to (Default None)
        :type freq:  float
        :type pin:   int

        :returns: Initialized SainSmart instance
        :rtype:   Class SainSmart

        .. note::
        The defaults are based on the SainSmart319 servo, accessible via the
        link in the class docstring. See Raspberry Pi and SainSmart
        documentation for acceptable parameter values for you equipment.

        .. note::
        Servos are not attached by default. If pin is not specified at
        initialization, SainSmart.attach() must be called before controlling
        servo. This is to minimize resource consumption before actual usage.
        """
        # validate frequency
        if freq >= 50 and freq <= 330:
            pass
        else:
            raise SainSmartClassException('Operating frequency out of range'
                                          + ' (50-330).')

        self.freq = freq
        self.min = 500   # minimum control pulsewidth in microseconds
        self.max = 2500  # maximum control pulsewidth in microseconds
        self.attached = False  # servo attachment flag

        if pin is not None:
            self.attach(pin)

    def attach(self, pin):
        """Initiates servo interface on a Broadcom numbered GPIO pin

        :param pin: Broadcom pin number servo is attached to
        :type pin:  int
        """
        self.pi = pigpio.pi()

        self.pin = pin
        self.pi.set_mode(self.pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.pin, self.freq)

        self.attached = True  # if no errors, servo should now be attached

    def detach(self):
        """Stops servo and releases PWM resources"""
        self.pi.stop()  # releases resources using by pigpio.py
        self.attached = False

    def write(self, microseconds):
        """Moves servo to position given in microseconds

        :param microseconds: Pulsewidth in microseconds (500-2500)
        :type microseconds: int
        """

        # validate position (limits from SainSmart documentation)
        if microseconds < 499 or microseconds > 2501:
            raise SainSmartClassException('Servo position out of range')

        # make sure servo is attached
        if not self.attached:
            raise SainSmartClassException('Servo is not attached')

        # set positon
        self.pi.set_servo_pulsewidth(self.pin, microseconds)
        self.postion = microseconds

        # turn off PWM
        sleep(0.02)  # determined experimentaly with sainsmart_test.py
        self.pi.set_servo_pulsewidth(self.pin, 0)

    def read(self):
        """Reads current servo position

        :returns: Current servo position in microseconds
        :rtype:  int

        .. note::
        This just returns the last value written to the servo. This is the only
        option, as SainSmart servos work in open loop control and cannot
        send back data.
        """
        return self.position


if __name__ == '__main__':
    print('This is a SainSmart object file!')
