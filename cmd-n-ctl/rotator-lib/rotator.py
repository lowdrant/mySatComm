"""
Object file for class interfacing with a 3-servo rotator

author: Marion Anderson
date:   2018-06-17
file:   rotator.py
"""
from __future__ import absolute_import, print_function

import time

import pigpio


class RotatorClassException(Exception):
    """Provide exceptions for Rotator class"""
    pass


class Rotator(object):
    """
    Interface to 3-servo antenna rotator using PiGPIO pwm methods.

    See this link for PiGPIO documentation:
    http://abyz.me.uk/rpi/pigpio/index.html

    See Raspberry Pi pinout here:
    https://pinout.xyz/#
    """

    def __init__(self):
        """Create basic antenna rotator instancece

        .. note::
        See Raspberry Pi and your servos' documentation for acceptable
        parameter values for your equipment.

        .. note::
        Servos are not attached by default. Run `rotator.attach()` to reserve
        system resources.
        """

        # assign pins NoneType by default
        self.pin_az1 = None
        self.pin_az2 = None
        self.pin_el = None

        # default positions (0 az, 0 el)
        self.az = 0
        self.el = 0

        # other parameters
        self.pi = None  # pigpio interface object
        self.attached = False

    def attach(self, pin_az1, pin_az2, pin_el):
        """Initiate rotator control interface.

        :param pin_az1: GPIO pin for 1st azimuth servo
        :param pin_az2: GPIO pin for 2nd azimuth servo
        :param pin_el:  GPIO pin for elevation servo

        :type pin_az1: int
        :type pin_az2: int
        :type pin_el:  int

        .. note::
        See Raspberry Pi pinout here: https://pinout.xyz/#
        """

        self.pi = pigpio.pi()  # reserving daemon resources

        self.pin_az1 = pin_az1
        self.pin_az2 = pin_az2
        self.pin_el = pin_el

        self.pi.set_mode(self.pin_az1, pigpio.OUTPUT)
        self.pi.set_mode(self.pin_az2, pigpio.OUTPUT)
        self.pi.set_mode(self.pin_el, pigpio.OUTPUT)

        self.attached = True  # if no errors, servos should now be attached

    def detach(self):
        """Stop servo and release PWM resources."""

        self.pi.stop()  # releases resources used by pigpio daemon
        self.attached = False

    def zero(self):
        """Move rotator to default position, 0deg Az, 0deg El."""

        self.writeRotator(0, 0)

    def calibrate(self):
        """Calibrate rotator by sequentially moving it to
        well-defined positions.
        """

        _ = input('Press enter to zero rotator: ')
        self.zero()

        # Azimuth calibration
        for az in (90, 180, 270, 360):
            input('Press enter to move to {0} degrees Azimuth: ')
            self.writeRotator(az, 0)
        print('Zeroing rotator, just in case...')
        time.sleep(0.25)
        self.zero()

        # Elevation calibration
        for el in (-10, 30, 45, 60, 90):
            input('Press enter to move to {0} degrees Elevation: ')
            self.writeRotator(0, el)
        print('Zeroing rotator, just in case...')
        time.sleep(0.25)
        self.zero()

    def writeRotator(self, az, el):
        """Move rotator to an orientation given in degrees.

        :param az: Azimuth angle
        :param el: Elevation angle

        :type az:  float
        :type el: float
        """

        if not self.attached:
            raise RotatorClassException('Rotator not attached!')

        # Input processing
        az = az % 360  # constrain azimuth to 360 degrees
        self.az = az
        self.el = el

        # Divide up the azimuth rotation between 2 servos
        # this is because servos can only move 180 degrees
        if az > 180:
            self._write_servo(self.pin_az1, 180)
            self._write_servo(self.pin_az2, az - 180)
        else:
            self._write_servo(self.pin_az1, az)
            self._write_servo(self.pin_az2, 0)

        self._write_servo(self.pin_el, el)

    def readAz(self):
        """Read current rotator azimuth in degrees.

        :returns: Rotator azimuth in degrees
        :rtype:   float

        .. note::
        This just returns the last value written to the rotator. This is the
        only option, as this class does not support feedback servos
        """

        return self.az

    def readEl(self):
        """Read current rotator elevation in degrees.

        :returns: Rotator elevation angle in degrees
        :rtype:   float

        .. note::
        This just returns the last value written to the rotator. This is the
        only option, as this class does not support feedback servos
        """

        return self.el

    def _deg_to_us(self, deg):
        """Converts degrees to microseconds.

        :param deg: Angle value in degrees
        :type deg:  float
        :returns:   Angle in microseconds
        :rtype:     float

        .. note::
        The mapping is a linear fit calculated using these two points:
        (0deg, 500us) and (180deg, 2500us).
        """

        if deg > 180 or deg < 0:
            except_str = 'Servo degree values must be in range [0, 180]'
            raise RotatorClassException(except_str)

        m = 200 / 18.0  # from (2500 - 500) / (180 - 0)
        b = 500         # 500us is minimum servo pulsewidth

        return m * deg + b

    def _write_servo(self, pin, degrees):
        """Internal helper method for moving servos.

        :param pin:     Broadcom pin number of servo being written
        :param degrees: Angle to move servo

        :type pin:      int
        :type degrees:  float
        """

        if degrees > 180 or degrees < 0:
            exceptstr = 'Servo degree values must be in range [0, 180]'
            raise RotatorClassException(exceptstr)

        # Sending command signal
        us = self._deg_to_us(degrees)
        self.pi.write_servo_pulsewidth(pin, us)

        # Unsetting command signal
        # (reduces risk of accidental servo response)
        time.sleep(0.2)  # experimentally determined delay
        self.pi.write_servo_pulsewidth(pin, 0)


if __name__ == '__main__':
    print('This is the Rotator class file!')
