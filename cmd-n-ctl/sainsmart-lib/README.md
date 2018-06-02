# sainsmart-lib
Python class unique to this repo. Used to communicate with SainSmart servos.

## Gotchas
```SainSmart.write()``` is in microseconds, not degrees. Look at the [SainSmart319 documentation](https://www.sainsmart.com/products/copy-of-all-purpose-digital-servo-sr318) for more details.

## Methods
Methods are pretty similar to the corresponding Arduino functions.

### Constructor
```
SainSmart(freq=50)
```
Initializes servo interface class. The communication frequency can be specified as any value between 50 and 330 (Hz). Defaults to 50Hz.

### attach
```
attach(int)
```
Reserves PWM resources and sets communication pin number.

### detach
```
detach()
```
Releases PWM resources.

### write
```
write(val)
```
Sends position command to servo in units of microseconds.

### read
```
read()
```
Returns the last input on write() call. Servos cannot communicate back, so the last command position is the only feasible read option.
