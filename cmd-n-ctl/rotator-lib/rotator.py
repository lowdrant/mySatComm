#! /usr/bin/env python3
"""
Object file for class interfacing with antenna rotator

author: Marion Anderson
date:   2018-06-17
file:   rotator.py
"""
from __future__ import absolute_import, print_function

import os
import time
from multiprocessing import Process, Lock

import pigpio


class RotatorClassException(Exception):
    """Provide exceptions for Rotator class"""
    pass


class Rotator(object):
    """
    Interface to antenna rotator using a stepper motor and a servo.

    See this link for PiGPIO documentation:
    http://abyz.me.uk/rpi/pigpio/index.html

    See Raspberry Pi pinout here:
    https://pinout.xyz/#
    """

    def __init__(self, pin_az, pin_el, pin_dir, step_angle=1.8, step_delay=5):
        """Create basic antenna rotator instancece

        :param pin_az: GPIO pin for incrementing step
        :type pin_azfwd: length-4 int array
        :param pin_el:  GPIO pin for elevation servo
        :type pin_el:  int
        :param pin_dir: GPIO pin controlling stepper direction
        :type pin_dir: int

        :param step_angle: Az control step angle in degrees (Default: 1.8)
        :type step_angle: float
        :param step_delay: Delay between phases in milliseconds (Default: 5)
        :type step_delay: float

        .. note::
        See Raspberry Pi and your motors' documentation for acceptable
        parameter values for your equipment.

        .. note::
        Servos are not attached by default. Run `rotator.attach()` to reserve
        system resources.
        """
        # Assigning motor params
        self.pin_az = pin_az
        self.pin_el = pin_el
        self.pin_dir = pin_dir
        self.step_angle = step_angle
        self.step_delay = step_delay

        # Determining current position
        homepath = os.environ['HOME']
        self.statepath = homepath + '/.satcomm/rotator-state.conf'
        if os.path.isfile(self.statepath):
            self.statefile = open(self.statepath, 'r+')
            state = self.statefile.read()
            self.az = float(state[state.index(':')+1:state.rindex(' ')])
            self.el = float(state[state.rindex(':')+1:])
        else:
            self.az = 0
            self.el = 0
            self.statefile = open(self.statepath, 'w')  # write first
            self._savestate()
            self.statefile.close()  # close and reopen to avoid errors
            self.statefile = open(self.statepath, 'r+')

        # other parameters
        self.pi = None  # pigpio interface object
        self.num_pts = 4  # internal const for _spline_trajectory()
        self.attached = False
        self.mutex = Lock()

    def attach(self):
        """Initiate rotator control interface.

        .. note::
        See Raspberry Pi pinout here: https://pinout.xyz/#
        """
        self.pi = pigpio.pi()  # reserving daemon resources

        # Set all pins to output
        self.pi.set_mode(self.pin_az, pigpio.OUTPUT)
        self.pi.set_mode(self.pin_dir, pigpio.OUTPUT)
        self.pi.set_mode(self.pin_el, pigpio.OUTPUT)

        # Force output low
        self.pi.set_servo_pulsewidth(self.pin_el, 0)
        self.pi.write(self.pin_az, 0)
        self.pi.write(self.pin_dir, 0)
        self.attached = True

    def detach(self):
        """Stop servo and release PWM resources."""
        self.pi.stop()  # releases resources used by pigpio daemon
        self.statefile.close()  # close file stream
        self.attached = False

    def zero(self):
        """Move rotator to default position: 0deg Az, 0deg El."""
        if not self.attached:
            raise RotatorClassException('Rotator not attached')
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

        Handles input processing and commanding. The individual commands
        update the state variables.

        :param az: Azimuth angle
        :type az:  float
        :param el: Elevation angle
        :type el:  float
        """
        if not self.attached:
            raise RotatorClassException('Rotator not attached!')

        # Input processing
        el += 90   # 0deg el is 90deg servo, b/c elevation goes up & down
        az %= 360  # angles wrap at 360deg

        # Command motors
        # use threading to allow simultaneous execution
        # TODO: Implement splining
        thread_az = Process(target=self._write_az, args=(az,))
        thread_el = Process(target=self._write_el, args=(el,))
        thread_az.start()
        thread_el.start()
        thread_az.join()
        thread_el.join()

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
        if degrees > 90 or degrees < -10:
            exceptstr = 'El angle is constrained between -10 and 90deg'
            raise RotatorClassException(exceptstr)

        # Move servo and then hold it in that position
        # TODO: Decide if resetting pulsewidth is necessary
        us = 200 / 18.0 * degrees + 500  # eq: (2500-500)/(180-0) + 500
        self.mutex.acquire()
        self.pi.set_servo_pulsewidth(self.pin_el, us)
        time.sleep(0.2)  # experimentally determined delay
        self.pi.set_servo_pulsewidth(self.pin_el, 0)
        self.mutex.release()

        # Save state
        self.el = degrees
        self.mutex.acquire()
        self._savestate()
        self.mutex.release()

    def _write_az(self, degrees):
        """Low level stepper azimuth control (internal method).

        :param degrees: Desired azimuth position in degrees
        :type degrees: float
        """
        # Choose rotation direction by minimizing distance
        cwdiff = abs(self.az - degrees)  # CW increment
        ccwdiff = abs(self.az - degrees + 360)  # CCW increment

        # Determine num steps and rotate
        # CW
        if cwdiff < ccwdiff:
            self.pi.write(self.pin_dir, 1)  # CW mode
            time.sleep(0.001)  # propagation delay
            steps = round(cwdiff / self.step_angle)  # how many steps
            for i in range(steps):
                self.mutex.acquire()
                self.pi.write(self.pin_az, 1)
                time.sleep(self.step_delay / 1000.0)  # delay in ms
                self.pi.write(self.pin_az, 0)
                self.mutex.release()
                time.sleep(self.step_delay / 1000.0)
        # CCW
        else:
            self.pi.write(self.pin_dir, 0)  # CCW mode
            time.sleep(0.001)  # propagation delay
            steps = round(ccwdiff / self.step_angle)  # how many steps
            for i in range(steps):
                self.mutex.acquire()
                self.pi.write(self.pin_az, 1)
                time.sleep(self.step_delay / 1000.0)
                self.pi.write(self.pin_az, 0)
                self.mutex.release()
                time.sleep(self.step_delay / 1000.0)

        # Record actual azimuth
        self.az = steps * self.step_angle
        self.mutex.acquire()
        self._savestate()
        self.mutex.release()

    def _savestate(self):
        """Overwrites rotator position to persistent file (internal method).

        .. note::
        Update az and el BEFORE calling this method.
        """
        self.statefile.seek(0)
        self.statefile.write('Az:' + str(self.az) + ' El:' + str(self.el))
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
