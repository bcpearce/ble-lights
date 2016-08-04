#!/usr/bin/python

import sys, time
from bluepy.btle import Peripheral

# 0x0043 register
# [0x56, red, green, blue, ???, 0xf0 for on or 0x0f for off, 0xaa]

class BleLed(Peripheral):

    SOLID_COLOR_HDL = 0x0043

    def norm_color(self, color):
        red, green, blue = color

        # normalize to 1-byte
        for c in [red, green, blue]:
            if c > 0xff:
                c = 0xff
            elif c < 0x00:
                c = 0x00

        return red, green, blue

    def set_solid_color(self, color=(0xff, 0xff, 0xff)):
        red, green, blue = self.norm_color(color)

        msg = str(bytearray([0x56, red, green, blue, 0x00, 0xf0, 0xaa]))
        self.writeCharacteristic(self.SOLID_COLOR_HDL, msg)


    def turn_off(self):
        msg = str(bytearray([0x56, 0x00, 0x00, 0x00, 0xff, 0x0f, 0xaa]))
        self.writeCharacteristic(self.SOLID_COLOR_HDL, msg)


if __name__ == "__main__":

    try:
        with open('ble_dev') as f:
            ble_dev = f.read().strip()
        light = BleLed(ble_dev)
        light.set_solid_color((0xff, 0xff, 0xff))
        time.sleep(2)
        light.turn_off()


    finally:
        light.disconnect()
