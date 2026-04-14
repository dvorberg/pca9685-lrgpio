#!/usr/bin/env python3

"""
### Overview
* The `Controller` class provides connectivity and access to the PWM
  outputs and the mode registers. It has methods to change some of the
  deviceʼs settings. The 16 outputs are available through subscrpipt
  (array access) syntax. 
* The `Output` class models an output and has properties to access the 
  on and off times as well as methods to turn the output fully on or
  fully off.
"""

import time, math

from i2cutils.device import SBC, Device
from i2cutils.bitpattern import ByteSpec, Byte, Word

from .abc import Controller, Output

# Datasheet 7.3 Register definitions
MODE1              = 0x00
MODE2              = 0x01
# SUBADDR* unsupported
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Datasheet 7.3.1 Mode register 1, MODE1
RESTART=7
EXTCLK=6
# AUTO_INCREMENT=5 unsupported.
SLEEP=4
# SUB* and ALLCALL unsupported as of yet.

# Datasheet 7.3.2 Mode register 2, MODE2
# Unsupported.

class ByteRegister(object):
    def __init__(self, register:int):
        self.register = register

    def __get__(self, device:Device, owner:object|None=None) -> Byte:
        return Byte(device.read_byte_data(self.register))

    def __set__(self, device:Device, value:ByteSpec) -> Byte:
        value = Byte(value)
        device.write_byte_data(self.register, value)
        return value

class ConfigurationBit(object):
    def __init__(self, register:ByteRegister, bit:int):
        self.register = register
        self.bit = bit

    def __get__(self, device:Device, owner:object|None=None) -> bool:
        return self.register.__get__(device, owner).get_bit(self.bit)

    def __set__(self, device:Device, value:bool) -> bool:
        old = self.register.__get__(device, None)
        new = old.set_bit_to(self.bit, value)
        
        # Do not write the restart bit, *unless* we *are* the restart bit.
        if self.bit != RESTART:
            new = new.set_bit_to(RESTART, False)

        self.register.__set__(device, new)
        
        return value
        
class Controller(Controller, Device):
    """
    Provide access to a PWM controller. 
    """
    
    mode1 = ByteRegister(MODE1)
    """
    Changes to the register (through the `ConfigurationBit` instances)
    below are not orchestrated to proper sequences.
    
    The mode register 2 is not supported, because I do not use any of its
    features. 
    """
    
    restart:bool = ConfigurationBit(mode1, RESTART)
    """
    Reading: Shows state of RESTART logic. See Section 7.3.1.1 for detail.<br>
    Writing: User writes logic 1 to this bit to clear it to logic 0. A user
       write of logic 0 will have no effect. See Section 7.3.1.1 for detail.

    0 (default): Restart disabled 1: Restart enabled
    """

    external_clock:bool = ConfigurationBit(mode1, EXTCLK)
    """
    Use the EXTCLK pin. Refer to the datasheet Table 5 for activation sequence.
    """

    sleep:bool = ConfigurationBit(mode1, SLEEP)
    """
    0: Normal mode <br>
    1: Low power mode. Oscillator off. Cf. footnotes to datasheet
       Table 5 for details. 
    """

    prescale:int = ByteRegister(PRESCALE)
    """
    The prescaler bits to program the PWM output frequency.
    """
    
    def __init__(self, sbc:SBC, i2c_bus:int, address:int):
        """
        Args:
            sbc: Either the lgpio module, a rgpio.sbc instance or a
                wrapper thereof.
            i2c_bus: Bus number
            address: The device’s address on that bus. 
        """
        super().__init__(sbc, i2c_bus, address)

        
    def __getitem__(self, idx:int) -> Output:
        """
        A controller is an array of 16 outputs. 
        """
        return Output(self, idx)

    def set_update_rate(self, update_rate_hz:int,
                        oscillator_frequency_mhz:float=25.0):
        """
        Set the prescaler bits to program the PWM output frequency. The
        PCA9685 has an internal oscillator running at 25Mhz. In case you
        want to use your own oscillator (and set the configuration bit
        accordingly), use the `oscillator_frequency_mhz` paramter. 
        """
        # Cf. to the datasheet 7.3.5 PWM frequency PRE_SCALE.
        osc_clock = oscillator_frequency_mhz * 1000000 # Puts the “mega” in MHz.
        prescale = osc_clock / (4096.0 * update_rate_hz) - 1.0
        prescale = math.floor(prescale + 0.5)
        
        assert 0x03 <= prescale <= 0xff, ValueError
        # “The maximum PWM frequency is 1526 Hz if the PRE_SCALE register is
        # set 0x03. The minimum PWM frequency is 24 Hz if the PRE_SCALE
        # register is set 0xFF” (Datasheet 7.3.5).

        self.sleep = True
        self.prescale = prescale
        self.sleep = False
        time.sleep(0.005)
        self.restart = True

        
class Output(Output):
    """
    Model one PWM output of the `Controller`. Use the `pwm_on` and
    `pwm_off` properties to set the PWM times. 
    """
    def __init__(self, controller:Controller, idx:int):
        self.controller = controller
        self._idx = idx

        # There are four bytes per output. 
        self._offset = self._idx * 4

    @property
    def pwm_on(self) -> Word:
        return self.controller.read_word_data(LED0_ON_L + self._offset)

    @pwm_on.setter
    def pwm_on(self, value:Word):
        # value = value & 0x0fff
        assert value <= 0x0fff, ValueError # 12 bit per channel
        self.controller.write_byte_data(LED0_ON_L + self._offset, value & 0xff)
        self.controller.write_byte_data(LED0_ON_H + self._offset, value >> 8)

    @property
    def pwm_off(self) -> Word:
        return self.controller.read_word_data(LED0_OFF_L + self._offset)

    @pwm_off.setter
    def pwm_off(self, value:Word):
        # value = value & 0x0fff
        assert value <= 0x0fff, ValueError # 12 bit per channel
        self.controller.write_byte_data(LED0_OFF_L + self._offset, value & 0xff)
        self.controller.write_byte_data(LED0_OFF_H + self._offset, value >> 8)
