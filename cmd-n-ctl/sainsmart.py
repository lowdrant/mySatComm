#! /usr/bin/env python
"""
Object file for class interfacing with SainSmart319 servos

author: Marion Anderson
date:   2018-05-30
file:   sainsmart.py
"""
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
        pigpio.pi.__init()

        self.pin = pin
        self.set_mode(self.pin, pigpio.OUTPUT)       # self.pin for implicit
        self.set_PWM_frequency(self.pin, self.freq)  # assignment validation

        self.attached = True  # if no errors, servo should now be attached

    def detach(self):
        """Stops servo and releases PWM resources"""
        self.stop()  # releases resources using by pigpio.py
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

        # TODO: Determine if SainSmart servos need pulsewidth set back to 0.
        # pigpio documentation states that set_servo_pulsewidth maintains a
        # value until it is changed.

    def read(self):
        """Reads current servo position

        Really just returns the last value written to the servo. This is really
        is the only option, as SainSmart servos work in open loop control and
        cannot send back data.

        Returns:
            (int): Current servo position in microseconds
        """
        return self.position


if __name__ == '__main__':
    print('This is a SainSmart object file!')
