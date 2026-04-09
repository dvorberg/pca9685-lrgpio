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

* [API Reference](https://dvorberg.github.io/pca9685-lrgpio/pca9685.html) 
* [PCA9685 datasheet](https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf)
* A hopefully growing number of examples in `examples/`. 

This project depends on my
[i2cutils-lrgpio](https://github.com/dvorberg/i2cutils-lrgpio) module.
