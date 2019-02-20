# rotator-lib

Python class unique to this repo. Used to communicate with servos in my homebrew setup

## Design Notes

This interface relies on 1 servo and 1 stepper. The servo controls elevation rotation, as it can only support ~180 degrees of rotation, and the stepper handles rotation, as it can rotate 360 degrees in either direction.

During setup, I recommend running the calibrate method. It will set the rotator to 0 degrees Azimuth, 0 degrees Elevation. You should then align the rotator with Absolute North for GPredict's oritentation calculations.

Due to the use of the `pigpiod` daemon, the detach method **must** be called at the end of rotator scripts. Otherwise the resources used won't be release and the Pi must be restarted.

## Methods

These methods are pretty similar to the Arduino servo methods.

```python
rotator()
```

Initializes rotator interface class.

```python
attach(int pin_az1, int pin_az2, int pin_el)
```

Reserves PWM resources and sets servo pin numbers. Call this before sending any commands to servo.

```python
detach()
```

Releases PWM resources. This **must** be called at the end of all interface scripts.

```python
writeRotator(int deg_az, int deg_el)W
```

Sends position command to rotator in units of degrees.

```python
readAz(), readEl()
```

Returns input to the last writeRotator() call. This class does not allow for servo feedback, so returning  last command position is the only feasible read option.
