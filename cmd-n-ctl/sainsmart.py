#! /usr/bin/env python
from __future__ import print_function, absolute_import

import pigpio

class SainSmartException(Exception):
    """SainSmart class generic exception"""
    pass

class SainSmart(pigpio.pi):
    """Interface to SainSmart 318 and 319 servomotors using PiGPIO.

    Inherits pigpio.pi class to allow access to other methods

    See this link for PiGPIO documentation:
    http://abyz.me.uk/rpi/pigpio/index.html

    And this link for SainSmart319 documentation:
    https://www.sainsmart.com/collections/robotics-cnc/products/copy-of-all-purpose-digital-servo-sr318
    """

    def __init__(self, freq=50):
        """Creates basic instance of SainSmart object.

        The defaults are based on the SainSmart319 servo, accessible via the
        link in the class docstring. See Raspberry Pi and SainSmart
        documentation for acceptable parameter values for you equipment.

        Inheritance from pigio.pi is not initiated in __init__ because the
        pigpio.pi class reserves resources from a daemon. It is initiated in
        SainSmart.attach(), where it is more clear that the resources are about
        to be utilized.

        Args:
            freq (int, default=50): Frequency (Hz) of servo operation

        Returns:
            SainSmart object instance
        """
        # validate frequency
        if freq >= 50 and freq <= 330:
            pass
        else:
            raise SainSmartException('Operating frequency out of range.')

        self.freq = freq
        self.min  = 500   # minimum control pulsewidth in microseconds
        self.max  = 2500  # maximum control pulsewidth in microseconds
        self.attached = False  # servo attachment flag

    def attach(self, pin):
        """Initiates servo interface on a Broadcom numbered GPIO pin

        Args:
            pin (int): The pin connected to the servo
        """
        pigpio.pi.__init()

        self.pin = pin
        self.set_mode(self.pin, pigpio.OUTPUT)       # use self.pin for implicit
        self.set_PWM_frequency(self.pin, self.freq)  # assignment validation

        self.attached = True  # if no errors, servo should now be attached

    def detach(self):
        """Stops servo"""
        self.stop()
        self.attached = False

    def write(self, microseconds):
        """Moves servo to position given in microseconds

        Args:
            microseconds (int): Pulsewidth in microseconds
        """
        # validate position (limits from SainSmart documentation)
        if microseconds < 500 or microseconds > 2500:
            raise SainSmartException('Servo position out of range')

        # make sure servo is attached
        if not self.attached:
            raise SainSmartException('Servo is not attached')

        self.set_servo_pulsewidth(self.pin, microseconds)
        self.postion = microseconds

    def read(self):
        """Reads current servo position

        Returns:
            (int): Current servo position in microseconds
        """
        return self.position


if __name__ == '__main__':
    print('This is a SainSmart object file!')
