"""
Access a PCA9685 LED controller through the i2c wrapper provided
by [rgpio](http://abyz.me.uk/lg/py_lgpio.html) or
[lgpio](http://abyz.me.uk/lg/py_rgpio.html).

This is a learning project of mine to understand I2C programming
better, and an API design exercise. I plan to use this in “production”
on my model railway, but I will only test it is as far as I use
it. Your milage may vary. Patches welcome.

The PCA9685 is designed to be a sophisticated dimmer for LEDs. It
turns them on and off in a rythmic fashion at high frequencies
referred to as Pulse Width Modulation (PWM). This will make them
appear darker or brighter to the human eye. The quality of its output
signal is high enough to create a control signal for a servo
motor. This is how I encountered the PCA9685: As key component of a
"Servo Driver" PCB and this is how I use it the most.

The controller has 16 PWM outputs each controled by two
12bit-values as stated in the [datasheet](https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf):

> There will be two 12-bit registers per LED output. These registers
> will be programmed by the user. Both registers will hold a value
> from 0 to 4095. One 12-bit register will hold a value for the ON
> time and the other 12-bit register will hold the value for the OFF
> time. The ON and OFF times are compared with the value of a 12-bit
> counter that will be running continuously from 0000h to 0FFFh (0 to
> 4095 decimal).
>
> The ON time […] will be the time the LED output will be asserted and
> the OFF time, which is also programmable, will be the time when the
> LED output will be negated. In this way, the phase shift becomes
> completely programmable. The resolution for the phase shift is
> 1⁄4096 of the target frequency.

Each of the 16 outputs can also be switched full on of fully off,
adding GP?O capability. (Well, itʼs not a GPIO. There is no input.) 

### Submodules
* The `pca9685.abc` module provides abstract base classes for forward
  declerations.
* The `pca9685.pca9685` module contains the actual logic. The
  user-facing interface consists of the `Controller` and `Output` classes.
"""

# Import the user-facing interface for convenience. 
from .pca9685 import Controller, Output

# These may be imported from here to convenience. 
from i2cutils.bitpattern import ByteSpec, Byte

