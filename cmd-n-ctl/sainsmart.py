#! /usr/bin/env python3
"""
Object file for class interfacing with SainSmart319 servos

author: Marion Anderson
date:   2018-05-30
file:   sainsmart.py
"""
<<<<<<< HEAD
=======
from __future__ import print_function, absolute_import
from time import sleep
>>>>>>> 2e69a758b8840ecd2e68871d49223b60e8eb61d8
import pigpio


class SainSmartException(Exception):
    """SainSmart class generic exception"""
    pass


<<<<<<< HEAD
class SainSmart(pigpio.pi):
=======
class SainSmart(object):
>>>>>>> 2e69a758b8840ecd2e68871d49223b60e8eb61d8
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

        You may notice that pigpio.pi.__init inheritance is not called here.
        This is because the pigpio.pi class reserves resources from a daemon.
        It is called in SainSmart.attach(), where it is more clear that the
        resources are about to be utilized.

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
        self.min = 500   # minimum control pulsewidth in microseconds
        self.max = 2500  # maximum control pulsewidth in microseconds
        self.attached = False  # servo attachment flag

    def attach(self, pin):
        """Initiates servo interface on a Broadcom numbered GPIO pin

        Args:
            pin (int): The pin connected to the servo
        """
        self.pi = pigpio.pi()

        self.pin = pin
<<<<<<< HEAD
        self.set_mode(self.pin, pigpio.OUTPUT)       # self.pin for implicit
        self.set_PWM_frequency(self.pin, self.freq)  # assignment validation
=======
        self.pi.set_mode(self.pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.pin, self.freq)
>>>>>>> 2e69a758b8840ecd2e68871d49223b60e8eb61d8

        self.attached = True  # if no errors, servo should now be attached

    def detach(self):
        """Stops servo and releases PWM resources"""
        self.pi.stop()  # releases resources using by pigpio.py
        self.attached = False

    def write(self, microseconds):
        """Moves servo to position given in microseconds

        Args:
            microseconds (int): Pulsewidth in microseconds
        """

        # validate position (limits from SainSmart documentation)
        if microseconds < 499 or microseconds > 2501:
            raise SainSmartException('Servo position out of range')

        # make sure servo is attached
        if not self.attached:
            raise SainSmartException('Servo is not attached')

        # set positon
        self.pi.set_servo_pulsewidth(self.pin, microseconds)
        self.postion = microseconds

<<<<<<< HEAD
        # TODO: Determine if SainSmart servos need pulsewidth set back to 0.
        # pigpio documentation states that set_servo_pulsewidth maintains a
        # value until it is changed.
=======
        # turn off PWM
        sleep(0.02)  # determined experimentaly with sainsmart_test.py
        self.pi.set_servo_pulsewidth(self.pin, 0)
>>>>>>> 2e69a758b8840ecd2e68871d49223b60e8eb61d8

    def read(self):
        """Reads current servo position

<<<<<<< HEAD
        Really just returns the last value written to the servo. This is really
        is the only option, as SainSmart servos work in open loop control and
        cannot send back data.
=======
        Just returns the last value written to the servo. This is the only
        option, as SainSmart servos work in open loop control and cannot
        send back data.
>>>>>>> 2e69a758b8840ecd2e68871d49223b60e8eb61d8

        Returns:
            (int): Current servo position in microseconds
        """
        return self.position


if __name__ == '__main__':
    print('This is a SainSmart object file!')
