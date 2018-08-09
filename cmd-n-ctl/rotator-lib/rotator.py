#! /usr/bin/env python3
"""
Object file for class interfacing with a 3-servo rotator

author: Marion Anderson
date:   2018-06-17
file:   rotator.py
"""
from __future__ import absolute_import, print_function

import os
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
        See Raspberry Pi and your motors' documentation for acceptable
        parameter values for your equipment.

        .. note::
        Servos are not attached by default. Run `rotator.attach()` to reserve
        system resources.
        """
        # assing pins NoneType by default
        self.pin_azfwd = None
        self.pin_azrev = None
        self.pin_el = None

        # determine current position
        homepath = os.environ['HOME']
        self.statepath = homepath + '/rotator-state.conf'
        self.statefile = open(self.statepath, 'r+')
        if os.path.isfile(self.statepath):
            state = self.statefile.read()
            self.az = float(state[state.index('Az: '):self.index(' ')])
            self.el = float(state[state.index('El: '):-1])
        else:
            self.az = 0
            self.el = 0
            self._savestate()

        # other parameters
        self.pi = None  # pigpio interface object
        self.attached = False
        self.num_pts = 4  # internal const for _spline_trajectory()

    def attach(self, pin_azfwd, pin_azrev, pin_el):
        """Initiate rotator control interface.

        :param pin_azfwd: GPIO pin for 1st azimuth servo
        :type pin_azfwd: int
        :param pin_azrev: GPIO pin for 1st azimuth servo
        :type pin_azrev: int
        :param pin_el:  GPIO pin for elevation servo
        :type pin_el:  int

        .. note::
        See Raspberry Pi pinout here: https://pinout.xyz/#
        """
        self.pi = pigpio.pi()  # reserving daemon resources

        self.pin_azfwd = pin_azfwd
        self.pin_azrev = pin_azrev
        self.pin_el = pin_el

        # all are output
        self.pi.set_mode(self.pin_azfwd, pigpio.OUTPUT)
        self.pi.set_mode(self.pin_azrev, pigpio.OUTPUT)
        self.pi.set_mode(self.pin_el, pigpio.OUTPUT)

        # explicitly turn off output
        self.pi.set_servo_pulsewidth(self.pin_el, 0)

        self.attached = True  # if no errors, servos should now be attached

    def detach(self):
        """Stop servo and release PWM resources."""
        self.zero()  # return to default position at end of script
        self.pi.stop()  # releases resources used by pigpio daemon
        self.statefile.close()  # close file stream
        self.attached = False

    def absoluteZero(self):
        """Source of truth zeroing function.

        Directly uses PiGPIO functions to avoid other system breakdowns in
        case of emergency.
        """
        if not self.attached:
            raise RotatorClassException('Error: rotator not attached')
        # TODO: Zero stepper motor
        # Directly command servos to 0 as a failure safeguard
        self.pi.set_servo_pulsewidth(self.pin_el, 1500)  # el 0 is halfway

    def zero(self):
        """Move rotator to default position, 0deg Az, 0deg El."""
        if not self.attached:
            raise RotatorClassException('Error: rotator not attached')
        self.write(0, 0)

    def calibrate(self):
        """Calibrate rotator by sequentially moving it to
        well-defined positions.
        """
        input('Press enter to zero rotator: ')
        self.zero()

        # Azimuth calibration
        for az in (90, 180, 270, 360):
            input('Press enter to move to {0} degrees Azimuth: '.format(az))
            for i in range(5):
                self.write(az/4*i, 0)
                time.sleep(0.125)

        input('Press enter to zero rotator again: ')
        time.sleep(0.25)
        self.zero()

        # Elevation calibration
        for el in (-10, 30, 45, 60, 80):
            input('Press enter to move to {0} degrees Elevation: '.format(el))
            self.write(0, el)
            for i in range(5):
                self.write(0, el/4*i)
                time.sleep(0.125)

        # Return to home position
        input('Calibration finished!\nPress enter to return to zero: ')
        self.zero()

    def write(self, az, el):
        """Move rotator to an orientation given in degrees.

        :param az: Azimuth angle
        :type az:  float
        :param el: Elevation angle
        :type el:  float
        """
        if not self.attached:
            raise RotatorClassException('Rotator not attached!')

        # TODO: Convert az control to stepper motor
        # Input processing
        az = az % 360  # constrain azimuth to 360 degrees
        if el < -10 or el > 90:
            raise RotatorClassException('El constrained to [-10, 90]')
        el += 90  # 0deg el is 90deg servo, b/c elevation goes up & down

        # Commanding servos
        # TODO: Implement splining
        self._write_az(az)
        self._write_el(el)

        # Saving state
        self.az = az
        self.el = el
        self._savestate()

    def _write_el(self, degrees):
        """Lowlevel servo elevation control (internal method).

        :param degrees: Angle to move servo
        :type degrees:  float

        .. note::
        This is the only function that directly writes to the servos (which
        must be done in microseconds). This allows the rest of the class to
        operate in degrees. It also keeps the code more Pythonic.

        .. note::
        The degrees to microseconds conversion uses a line fit with two points:
        (0deg, 500us), (180deg, 2500us).
        Therefore the coefficients are:
        m = (2500 - 500) / (180 - 0) = 200 / 18
        b = 500
        """
        if degrees > 180 or degrees < 0:
            exceptstr = 'Angle {0} out of range [0, 180]'.format(degrees)
            raise RotatorClassException(exceptstr)

        us = 200 / 18.0 * degrees + 500  # eq: (2500-500)/(180-0) + 500
        self.pi.set_servo_pulsewidth(self.pin_el, us)

        # Unsetting command signal
        # (reduces risk of accidental servo response)
        time.sleep(0.2)  # experimentally determined delay
        self.pi.set_servo_pulsewidth(self.pin_el, 0)

    # TODO: Implement _write_az method
    def _write_az(self, degrees):
        """Lowlevel stepper motor azimuth control (internal method).

        :param degrees: Desired azimuth position in degrees
        :type degrees: float
        """
        raise NotImplementedError('Need to do stepper implementation!!')

    def _savestate(self):
        """Overwrites rotator position to persistent file.

        .. note::
        Update az and el BEFORE calling this method.
        """
        self.statefile.seek(0)
        self.statefile.write('Az: ' + str(self.az) + 'El: ' + str(self.el))
        self.statefile.flush()

    # TODO: Test spline generation
    def _spline_trajectory(self, p0, pf, dt=0.25):
        """Generate a smoothed servo movement trajectory over time dt.

        :param p0: Initial angular position of servo in degrees.
        :type p0:  float
        :param pf: Final angular position of servo in degrees.
        :type pf:  float
        :param dt: Time to reach final position in seconds. (Default 0.25)
        :type dt:  float

        :returns: tuple of positions in degrees
        :rtype: float tuple

        .. note::
        These equations use the assumption that initial and final velocities
        are 0. You should be able to find them in any robotics text covering
        trajectory generation for manipulators.

        .. note::
        The delay time between movements should be dt / Rotator.num_pts.
        All movements are in equal amounts of time
        """
        # default case: p0 = pf
        coeffs = [0] * self.num_pts  # spline coefficient array
        degrees = [p0] * self.num_pts  # trajectory

        # movement case
        if p0 != pf:
            # spline coefficients in degrees:
            coeffs[3] = p0
            coeffs[2] = 0
            coeffs[1] = 3/pow(dt, 2) * (pf - p0)
            coeffs[0] = 2/pow(dt, 3) * (-pf + p0)

            # computing trajectory points:
            # skip 1st value because it's just p0, and that is covered in
            # the default case above
            for i in range(1, self.num_pts):
                t = dt / self.num_pts * i  # time in trajectory
                degrees[i] = (coeffs[0] * pow(t, 3) + coeffs[1] * pow(t, 2) +
                              coeffs[2] * t + coeffs[3])

        return tuple(degrees)


if __name__ == '__main__':
    print('This is the Rotator class file!')
