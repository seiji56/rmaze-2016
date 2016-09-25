#!/usr/bin/env python3

from Adafruit_I2C import Adafruit_I2C

class Melexis:
    def __init__(self, addr=0x5A, fahrenheit=False):
        self._i2c = Adafruit_I2C(addr)
        self.mode = fahrenheit

    def readAmbient(self):
        return self._readTemp(0x06)

    def readObject(self):
        return self._readTemp(0x07)

    def readObject2(self):
        return self._readTemp(0x08)

    def getDifference(self):
        """Returns how much warmer the object is than the ambient
        temperature."""
        return self.readObject() - self.readAmbient()

    def _readTemp(self, reg):
        temp = self._i2c.readS16(reg)
        temp = temp * .02 - 273.15
        if self.mode:
            return (temp * 9 / 5) + 32
        else:
            return temp
